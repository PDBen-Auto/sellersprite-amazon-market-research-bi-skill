# SellerSprite Data Contract

## Logical Inputs

- `standard.xlsx`: SellerSprite competitor lookup standard export.
- `detail.xlsx`: detailed export containing monthly sales, sales amount, and price sheets.
- `as_of`: cutoff used to derive the last completed month.
- `scope_manifest`: marketplace, category/vehicle boundary, inclusions, exclusions, ASIN batches, and sources.
- `keyword_evidence.csv`: clustered SellerSprite keyword evidence with search volume, growth, purchase, competition, PPC, and frequent ASINs.
- `candidate_manifest.csv`: child-level discovery universe with parent ASIN, relevance decision/reason, detail availability, and Listing attributes.
- `type_map` and `fitment_map`: optional stable mappings keyed by child or parent ASIN.

Run the normalizer separately for `category_baseline`, `core_direct`, and any `adjacent_substitute` layer. Never merge their totals before calculating explicit coverage.

## Normalization Command

```powershell
python scripts/normalize_sellersprite_exports.py `
  --standard "path/to/standard.xlsx" `
  --detail "path/to/detail.xlsx" `
  --scope-manifest "path/to/candidate_manifest.csv" `
  --include-decisions "core_direct" `
  --output-dir "path/to/normalized" `
  --as-of 2026-09-21 `
  --market-name "Product category or vehicle" `
  --marketplace "Amazon US" `
  --rank-window-months 3
```

The parser identifies monthly columns by `YYYY-MM` or `YYYY-MM($)` and ASINs by value pattern because SellerSprite workbook labels may be localized or malformed.

When a scope manifest is supplied, only the listed decisions enter the fact table. Even without a manifest, standard-export rows are restricted to child/parent ASINs present in the detailed export; standard-only rows cannot create zero-sales parents.

## Parent-Month Rule

Apply the same rule independently to units and SellerSprite sales amount:

1. Resolve each child row to parent ASIN; use the child only when no parent exists.
2. Group rows by `parent ASIN + month + metric`.
3. Ignore blank cells but preserve observed zero.
4. If sibling values agree, keep one value.
5. If sibling values disagree, select the maximum visible value and write a conflict record containing metric, parent, month, selected value, and every child value.

Siblings are never summed. The maximum-visible-value rule limits repeated parent history in SellerSprite variant exports; it does not prove Amazon settlement accuracy.

## Metric Definitions

- `units`: parent-deduplicated SellerSprite monthly sales units.
- `seller_sprite_sales_amount`: parent-deduplicated monthly sales amount from the detailed sales-amount sheet.
- `representative_parent_price`: median positive historical price across the parent's exported children; standard-export median price fallback.
- `modeled_gmv`: parent-deduplicated units multiplied by representative parent price.
- `sales_weighted_asp`: SellerSprite sales amount divided by deduplicated units when both are complete.
- `modeled_asp`: modeled GMV divided by units.
- `listing_average_price` and `listing_median_price`: listing-level statistics; never label them ASP.

SellerSprite sales amount and modeled GMV are separate series. If the sales-amount sheet is absent, sales-amount competition and ranking momentum are `N/A`; do not silently substitute modeled GMV.

## Time Rules

- Last completed month is the calendar month before `as_of`.
- Exclude the in-progress month from annual/YTD, YoY, competition, concentration, and rank windows.
- A full year requires all 12 months. Partial years display exact coverage, such as `2025 Jan-Nov (11M)`.
- Same-period YoY uses identical month numbers in adjacent years. Missing prior months yield `N/A`.
- Annual/YTD totals must reconcile to the displayed monthly rows.
- Newly collected December data is merged by parent/month and compared with overlapping historical exports before inclusion.

## Count Rules

- `child_asin_count`: distinct returned listing ASINs.
- `parent_asin_count`: distinct resolved parents.
- `active_parent_count`: parents with positive units in the stated period.
- An observed zero remains an observation but is not active.
- A missing value is not zero and cannot be used in completeness tests.
- Historical `new product` status uses the 365 days ending at each displayed period end, not today's date.

## Competition Contract

Brand competition defaults to the latest completed month's parent-deduplicated SellerSprite sales amount:

- Parent share = parent sales amount / observed direct-market sales amount.
- Brand share = sum of each brand's deduplicated parent sales amount / observed direct-market sales amount.
- CR3/CR5 = sum of top 3/5 shares.
- HHI = sum of squared percentage shares.

Unit competition may be shown as a secondary view. It must not replace the declared sales-amount basis. If brand mapping is incomplete, show coverage and `Unknown` rather than silently discarding rows.

## Global Rank Momentum Contract

Ranking momentum is a standalone analytical dimension, not an input to commercial-opportunity scoring unless the user explicitly requests a documented model.

For default `rank_window_months = 3`:

1. Take the latest six completed sales-amount months.
2. Define the global universe as every parent with an observed value in all six months. Observed zero is valid; any blank excludes the parent.
3. Sum months 1-3 into `prior_sales_amount` and months 4-6 into `recent_sales_amount`.
4. Rank both windows descending by sales amount, using stable parent-ASIN tie breaking and competition ranking for equal values.
5. Calculate `rank_change = prior_rank - recent_rank`; positive means improvement.
6. Store `global_denominator` on every row.

Dashboard filters may hide rows but must never recompute these ranks or the denominator. Label the result `Calculated sample sales-amount rank; not Amazon BSR.`

## Output Schemas

### `parent_monthly.csv`

`parent_asin, brand, title, month, units, seller_sprite_sales_amount, representative_price, modeled_gmv`

### `market_monthly.csv`

`month, units, seller_sprite_sales_amount, modeled_gmv, active_parents, unit_parent_coverage, sales_amount_parent_coverage, unit_yoy, sales_amount_yoy, gmv_yoy`

### `parent_current.csv`

Parent metadata plus latest-month `units`, `seller_sprite_sales_amount`, `modeled_gmv`, and their separate shares.

### `rank_momentum.csv`

`parent_asin, brand, title, url, image, prior_months, recent_months, prior_sales_amount, recent_sales_amount, prior_rank, recent_rank, rank_change, sales_amount_change, sales_amount_yoy, global_denominator`

### `conflicts.csv`

`parent_asin, month, metric, selected, child_values`

### `dashboard_data.json`

Contains `metadata`, `parent_monthly`, `market_monthly`, `annual`, `same_period`, `parent_current`, `competition`, `rank_momentum`, and `data_quality`.

### Discovery outputs

- `keyword_evidence.csv`: one row per mined keyword with cluster and relevance flag.
- `candidate_manifest.csv`: one row per child ASIN with `core_direct`, `adjacent_substitute`, `excluded_noise`, or `review`.
- `parent_scope_manifest.csv`: parent-deduplicated candidate view.
- `target_child_asins.txt` and `target_parent_asins.txt`: accepted targets, limited to detailed-export coverage by default.
- `discovery_summary.json`: source files, seed inputs, counts, keyword clusters, decisions, targets, and limitations.

## Category And Fitment Dimensions

- Preserve L2, L3, leaf category, vehicle, generation, model year, fitment, product type, and marketplace as separate fields where available.
- A row may be included in multiple discovery queries but must enter a statistical universe only once.
- US/CA/MX totals are separate; an uncollected marketplace is `N/A`.
- Project-specific excluded brands/ASINs are applied through the scope manifest and documented in the quality section.

## Layer Coverage

For matching periods and metric methods:

- `core_unit_coverage = core_direct_units / category_baseline_units`
- `core_sales_amount_coverage = core_direct_sales_amount / category_baseline_sales_amount`
- `core_child_coverage = core_direct_children / category_baseline_children`
- `core_parent_coverage = core_direct_parents / category_baseline_parents`

Coverage is diagnostic, not proof of completeness. If scopes, periods, marketplaces, or methods differ, return `N/A`.

## Reconciliation Gate

Before publishing, verify:

- Category baseline, core direct, and adjacent totals are not combined.
- Child counts, parent counts, active parents, and new products use declared grains.
- Parent-month rows sum to market-month rows.
- Monthly rows sum to annual/YTD rows.
- Same-period YoY uses identical month sets.
- Type and L3 totals reconcile to their selected universe.
- Brand competition is based on SellerSprite sales amount.
- Ranking denominator is fixed and contains only complete parents.
- SellerSprite sales amount, modeled GMV, listing prices, and ASP retain distinct names.
