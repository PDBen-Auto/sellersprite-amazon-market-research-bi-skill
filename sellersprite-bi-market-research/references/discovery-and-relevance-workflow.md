# Keyword Discovery And Relevance Workflow

Use this workflow when the user starts with a category idea, one seed keyword, and one or more core competitor ASINs rather than a finished ASIN universe.

## 1. Define The Product Job Before Searching

Write a short project definition containing:

- Marketplace and seed keyword.
- Seed/core competitor ASINs and why they represent the intended product.
- Customer job and required outcome, such as `record + transcribe + summarize`.
- Required category or physical form.
- Core-direct, adjacent/substitute, and excluded-noise definitions.
- Attribute dimensions that matter for filtering: form factor, storage, compatible devices, transcription offer, subscription claim, use case, size, weight, or fitment.

This definition is provisional. Discovery may expose missing terms, but keyword results never define the market boundary by themselves.

## 2. Expand And Cluster Keywords

Use SellerSprite keyword mining on the seed phrase and, when useful, on the seed ASIN. Export the full result rather than copying a few visible rows.

Cluster relevant phrases into stable intent groups:

- Generic category
- AI outcome: transcription, summary, note taking, translation, AI documents
- Use case: meeting, call, lecture, interview, classroom
- Form factor: card, magnetic, wearable, pin, pocket, pen
- Commercial constraint: no subscription, free minutes, unlimited, offline
- Brand/product family
- Accessory/noise

Keep search volume, growth, purchases, purchase rate, product count, PPC evidence, and frequent ASINs. Keyword purchases are demand evidence, not direct-ASIN sales and not category TAM.

## 3. Build The Candidate Universe

Combine and deduplicate candidate ASINs from:

1. Seed/core competitor family and its parent/children.
2. Frequent ASINs in relevant keyword clusters.
3. SellerSprite competitor lookup for the seed keyword and high-signal long tails.
4. Same-category products visible on the seed listing when available.

Record query, source, rank/position, child ASIN, resolved parent ASIN, and discovery reason. A candidate appearing in multiple queries enters the manifest once.

## 4. Extract Listing Attributes

Use the SellerSprite standard export and, when needed, the Amazon listing title/bullets to preserve:

- Brand, title, category path, leaf category, parent/child relationship
- Variation/SKU and structured attributes
- Storage, compatible devices, format, color
- Product and package dimensions/weight
- Price, rating, reviews, launch date, fulfillment
- Project-specific attributes such as wearable, transcription, summary, free minutes, subscription, app dependency, or bundle

Do not infer a feature only from brand or price. Mark unavailable values as `Unknown`.

## 5. Grade Relevance

Every child and parent receives one of four decisions:

- `core_direct`: same physical product job and required outcome.
- `adjacent_substitute`: solves part of the job or uses a meaningfully different product structure.
- `excluded_noise`: accessories, unrelated categories, keyword stuffing, bundles that distort single-device economics, or other false matches.
- `review`: evidence is insufficient or conflicting.

Apply gates in this order:

1. Explicit project overrides.
2. Category and accessory/bundle exclusions.
3. Required customer-outcome terms and verified Listing attributes.
4. Trusted direct-product brands only as supporting evidence, never as the sole global rule.
5. Adjacent signals.
6. Manual review for the remainder.

Preserve the reason and score. Never silently delete excluded rows; keep them in the candidate manifest so the boundary is auditable.

## 6. Run The Deterministic Discovery Helper

Prepare a project-specific JSON rules file and run:

```powershell
python scripts/discover_sellersprite_market.py `
  --keyword-export "path/to/keyword-mining.xlsx" `
  --competitor-export "path/to/competitor-standard.xlsx" `
  --detail "path/to/selected-detail.xlsx" `
  --rules "path/to/discovery-rules.json" `
  --seed-keyword "ai voice recorder" `
  --seed-asin "B0FYQ4Y2ZZ" `
  --output-dir "path/to/discovery"
```

The helper emits keyword evidence, child candidates, parent scope, and target ASIN files. When a detailed export is supplied, target files are limited to candidates with detail coverage unless `--allow-without-detail` is explicitly used.

Example rules:

```json
{
  "required_category_terms": ["digital voice recorders"],
  "exclude_category_terms": ["laptops"],
  "core_title_terms": ["transcrib", "summar", "note taker", "ai docs"],
  "adjacent_title_terms": ["noise reduction", "voice activated recorder"],
  "exclude_title_terms": ["case", "charger", "combo", "bundle"],
  "core_brands": ["plaud", "pocket", "soundcore"],
  "overrides": {
    "B0EXAMPLE1": {
      "decision": "excluded_noise",
      "reason": "Accessory verified from Listing"
    }
  }
}
```

Rules are project evidence, not universal product truth. Inspect `review` rows and high-sales exclusions before finalizing the scope.

## 7. Export And Normalize The Accepted Universe

Submit the accepted child ASIN list to SellerSprite and request both standard and detailed exports. If a broader standard export is paired with a selected detailed export, the normalizer must restrict standard metadata to the detailed child/parent universe.

Pass the audited manifest into normalization:

```powershell
python scripts/normalize_sellersprite_exports.py `
  --standard "path/to/standard.xlsx" `
  --detail "path/to/detail.xlsx" `
  --scope-manifest "path/to/candidate_manifest.csv" `
  --include-decisions "core_direct" `
  --output-dir "path/to/normalized" `
  --as-of 2026-09-21 `
  --market-name "AI voice recorder direct sample" `
  --marketplace "Amazon US"
```

For comparative BI, normalize core and adjacent layers separately. Do not combine them into one market total.

## 8. Publish Discovery Coverage Honestly

The dashboard must show:

- Seed keyword and seed ASIN
- Number of keyword rows, candidates, detailed children, included parents, adjacent parents, exclusions, and review rows
- The exact market-layer definitions and active attribute filters
- Whether the sample is top-N, query-limited, or category-validated
- A warning that keyword and competitor-query samples are not complete category TAM

Stop capacity claims when the candidate universe or detailed-export coverage is incomplete. A useful direct-competitor sample can still support positioning, product-attribute, and concentration analysis when labeled correctly.
