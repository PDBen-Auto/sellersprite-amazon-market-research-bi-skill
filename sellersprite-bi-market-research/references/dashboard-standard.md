# BI Dashboard Standard

Deliver one responsive, self-contained HTML file that opens directly through `file://`. Inline CSS, JavaScript, data, SVG, and Canvas code. Do not require Power BI, localhost, a local API, external chart CDN, or external fonts.

## Information Architecture

Recommended pages or tabs:

1. `Overview`: scope, period, marketplace, core KPIs, annual comparison, trend, and confidence.
2. `YoY & Trend`: full-year/YTD/same-period units and SellerSprite sales amount, monthly line/area charts, seasonality, and exact month coverage.
3. `Category Structure`: L2/L3/leaf hierarchy, product-type mix, price bands, launch cohorts, and `Unknown` coverage.
4. `Brand Competition`: parent-deduplicated sales-amount share, CR3/CR5/HHI, brand trend, and parent drillthrough. Units are secondary.
5. `Commercial Opportunities`: demand, growth, competitive whitespace, price/profit structure, product gaps, and evidence quality. Do not silently include rank momentum.
6. `Ranking Momentum`: fixed-universe prior/recent rank, rank change, sales-amount change, global denominator, and completeness notes.
7. `Parent ASIN Database`: product image, parent ASIN, children, brand, title, Amazon link, L3/type/fitment, price, rating, reviews, launch date, fulfillment, units, sales amount, modeled GMV, and share.
8. `Metric & Data Quality`: formulas, source files, conflicts, missing months, exclusions, marketplace gaps, reference-BI differences, and evidence levels.

Focus BI may add reviews, user/JTBD analysis, off-Amazon evidence, product roadmap, patent/design-around, unit economics, and launch/advertising scenarios. Basic BI pages remain intact.

## Data-First Layout

- Use charts and compact KPI rows before explanatory prose.
- Move long methods and caveats to the final quality page. Use tooltips, info icons, footnotes, and concise annotations near data.
- Keep page headings compact; avoid marketing hero layouts, decorative cards, nested cards, large empty regions, gradients, and ornamental backgrounds.
- Use restrained neutral surfaces, one semantic color for positive change, one for negative change, and consistent category/vehicle colors.
- Pie/donut charts suit small share sets; sorted bars suit ranked categories/brands; line charts suit time; slope/dumbbell charts suit rank change; tables suit exact values.
- Always provide a table or accessible tooltip for exact chart values.

## Required Global Filters

Use a stable top filter bar with only relevant dimensions:

- Vehicle/category universe
- Marketplace/country
- Period: full year, YTD, same-period, month
- Market layer
- Keyword intent cluster or discovery source when discovery evidence is present
- L2/L3/leaf category
- Product type
- Project-specific Listing attributes such as form factor, storage, compatible device, transcription offer, subscription claim, or fitment
- Brand
- Parent ASIN/title/fitment search
- Launch cohort and price band

Filters must update KPIs, charts, table totals, legends, empty states, and URL/hash state together. Reset must restore a declared default. Cross-filtering a chart must visibly update all dependent views.

Rank-page filters are display filters only. They cannot recompute `prior_rank`, `recent_rank`, `rank_change`, or `global_denominator`.

## Drillthrough And Product Images

- Clicking a brand, category, type, chart segment, or rank row opens or filters the parent-ASIN detail view.
- The detail view shows the representative parent image plus child count/list; do not repeat child sales into totals.
- Product images need fixed aspect-ratio boxes, `object-fit: contain`, lazy loading, meaningful alt text, and a graceful placeholder when unavailable.
- Amazon links open the relevant product in a new tab. Keep ASIN visible as text for copying and verification.
- A breadcrumb or back action must return to the prior filtered view without losing context.

## Chart Rendering Contract

- Every chart container has an explicit stable height, responsive width, and nonzero minimum dimensions before rendering.
- Render after the target page is visible. Re-render or resize charts on tab changes, filter updates, window resize, and orientation change.
- Use one embedded data object and shared filter state; do not hardcode independent chart totals.
- Empty filtered results show an explicit `No matching data` state, not a blank white panel.
- A chart failure must expose a compact error/fallback table rather than leaving the section empty.
- Legends and labels must remain readable at desktop and mobile widths without overlapping controls.

## Core Visuals

- Annual units and SellerSprite sales amount: grouped bars with YoY labels.
- Monthly trend: two synchronized line charts or an explicit metric switch; never place incompatible scales on one unlabeled axis.
- L3/category structure: sorted horizontal bars, treemap, or sunburst with drilldown and percentage/amount tooltips.
- Brand competition: sales-amount donut for top brands plus sorted brand bars and trend; group small residuals only when the threshold is disclosed.
- Product-type mix: donut or 100% stacked bar by period, with `Unknown` visible.
- Price distribution: histogram or banded bar with units and sales amount switch.
- Rank momentum: dumbbell/slope chart plus full detail table, labeled as calculated sample rank rather than Amazon BSR.
- Parent database: image table/grid with column controls and export-ready exact values.

## Ranking Detail Requirements

- Show all complete-universe parents; never truncate permanently at 50.
- Provide page-size choices `50`, `100`, `250`, and `All`, plus page navigation, total rows, and current range.
- Default sort may use largest positive rank change or recent rank, but the global denominator remains fixed.
- Show prior/recent window labels, prior/recent sales amount, prior/recent global rank, rank change, sales-amount change, and completeness status.
- Missing-window parents may appear in a separate excluded/N/A list, not in the rank denominator.

## Scope And Metric Banner

The first screen must expose, without long prose:

- Market/category or vehicle name
- Marketplace and currency
- Data cutoff and last completed month
- Selected period and exact month count
- Category-baseline and core-direct parent counts
- Core coverage against the baseline
- Discovery sample counts: keyword rows, candidate children, detailed children, included/adjacent/excluded/review parents
- Active exclusions and data-quality status

Use tooltips for definitions. If the category baseline is incomplete, mark capacity as `N/A` or sample coverage rather than TAM.

## Responsive And Accessibility QA

Test at minimum around `1440x1000` and `390x844`:

- No horizontal page overflow, clipped controls, overlapping text, or chart labels outside their bounds.
- Every tab and cross-filter updates the correct data and has a usable empty state.
- Charts are nonblank on initial load and after navigating away and back.
- Product images load or fall back cleanly; links resolve.
- Tables paginate, sort, filter, and display all expected records.
- Keyboard focus is visible; icon-only controls have labels/tooltips; color is not the only status signal.
- No console errors, malformed encoding, or unhandled `null`/`NaN` values.
- KPI, chart, table, JSON, and CSV totals agree.
- Full-year, YTD, same-period, and partial-year labels are unambiguous.
- No username, password, cookie, token, authorization header, or browser-profile path appears in source or visible output.

## Delivery And Versioning

- Name each revision distinctly and keep earlier user-facing versions unless deletion is explicitly requested.
- Verify the final HTML and its embedded data from the exact delivery path.
- Static HTML is delivered as a direct file link; do not start a localhost server merely for preview.
