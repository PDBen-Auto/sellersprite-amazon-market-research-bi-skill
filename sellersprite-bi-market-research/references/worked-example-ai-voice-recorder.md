# Worked Example: AI Voice Recorder Market Discovery To BI

This reference turns the `AI Voice Recorder` project into a reusable worked method. It illustrates how to apply the general workflow; it does not make Plaud-specific brands, keywords, or exclusion rules universal defaults for other categories.

## 1. Project Definition

Use the following project scope as the starting hypothesis:

| Field | Worked-example value |
| --- | --- |
| Marketplace | Amazon US |
| Seed keyword | `ai voice recorder` |
| Seed/core ASIN | `B0FYQ4Y2ZZ` |
| Core customer job | Physically record speech and produce transcription plus summary, AI notes/documents, or translation |
| Core product form | Dedicated portable recording device; card, magnetic, wearable, pin, pocket, or pen form factors may qualify |
| Core direct market | Dedicated recorders whose Listing supports both recording and an AI information outcome |
| Adjacent/substitute market | Traditional digital recorders that mainly use `AI` for noise reduction, voice activation, or audio cleanup without a verified transcription/summary workflow |
| Excluded noise | Laptops bundled with recorders, cases/chargers/accessories, keyword-stuffed unrelated electronics, and multi-device bundles that distort single-device economics |
| Unit of market analysis | Parent ASIN; child ASINs are retained for discovery and export coverage auditing |

Before collection, write these values into the project `scope_manifest` and `discovery_rules`. If evidence changes the boundary, update the manifest and preserve the reason rather than silently changing the definition.

## 2. Keyword Expansion And Intent Clustering

Run SellerSprite keyword mining with the seed phrase and, when available, reverse-search the seed ASIN. Keep the complete export and assign relevant rows to these intent clusters:

| Cluster | Examples of evidence to retain | Research use |
| --- | --- | --- |
| Generic category | `ai voice recorder`, `voice recorder with transcription` | Defines the broad discovery pool, not category TAM |
| AI outcome | transcription, summary, note taking, AI documents, translation | Tests whether the Listing delivers the required information outcome |
| Use case | meeting, call, lecture, interview, classroom | Supports use-case filters and product positioning |
| Form factor | card, magnetic, wearable, pin, pocket, pen | Supports physical-product segmentation |
| Commercial constraint | no subscription, free minutes, unlimited, offline | Supports plan/offer filters; claims require Listing evidence |
| Brand/product family | Plaud and other discovered product/brand terms | Finds competitor families; brand alone never proves relevance |
| Accessory/noise | case, holder, charger, microphone, noise reduction | Helps identify accessories, traditional recorders, and false matches |

For every keyword preserve query source, cluster, relevance decision, search volume, growth, purchases, purchase rate, product count, PPC evidence, and frequent ASINs where present. Treat keyword purchases as demand evidence only. Do not add them to product sales or describe the query sample as full category capacity.

## 3. Candidate ASIN Discovery

Build one deduplicated child-ASIN candidate universe from:

1. The seed ASIN, its resolved parent, and visible variations.
2. Frequent ASINs from relevant keyword clusters.
3. SellerSprite competitor results for the seed keyword and high-signal long-tail phrases.
4. Related or comparable products visible on the seed Listing when accessible.
5. Additional ASINs discovered from competitor families after confirming that their Listings serve the same customer job.

Record each discovery event before deduplication: query, source, rank/position, child ASIN, resolved parent ASIN, and discovery reason. Merge duplicate ASINs into one candidate row while retaining all source evidence.

## 4. Listing Attribute Extraction

Use the SellerSprite standard export as the main structured source and inspect Amazon Listing title/bullets only when required to resolve ambiguity. Preserve at least:

- Brand, title, category path, leaf category, parent/child relation, and variation.
- Form factor and wearable/magnetic/card/pin/pen signals.
- Storage capacity and compatible devices.
- Transcription, summary, note/document, and translation claims.
- Included or free transcription minutes, subscription wording, offline claims, and app dependency.
- Product and package dimensions/weight.
- Bundle contents, quantity, and whether the offer represents one recorder or multiple devices.
- Price, rating, reviews, launch date, fulfillment, image, and product URL.

Missing attributes remain `Unknown`. Do not infer transcription, subscription terms, or compatibility from price, brand, imagery, or an isolated occurrence of the word `AI`.

## 5. Four-Layer Relevance Decision

Apply rules in order and preserve the deciding evidence:

1. `core_direct`: a dedicated physical recorder with verified recording plus transcription and at least one further AI information outcome such as summary, notes/documents, or translation.
2. `adjacent_substitute`: a recorder that solves only part of the job, especially products where `AI` refers mainly to noise reduction or voice activation.
3. `excluded_noise`: accessories, unrelated device categories, laptop/recorder bundles, multi-recorder packs that distort unit economics, and keyword-stuffed false matches.
4. `review`: evidence is missing, conflicting, or insufficient to make one of the preceding decisions.

The exact project rule may be stricter or broader, but changes must be explicit in the manifest. Review every high-sales exclusion and every `review` row before publishing a core-market total.

Example project rules, to be edited from evidence rather than copied blindly:

```json
{
  "required_category_terms": ["digital voice recorders"],
  "exclude_category_terms": ["laptops"],
  "core_title_terms": ["transcrib", "summar", "note taker", "ai docs", "translation"],
  "adjacent_title_terms": ["noise reduction", "voice activated recorder"],
  "exclude_title_terms": ["case", "holder", "charger", "combo", "bundle"],
  "overrides": {
    "B0EXAMPLE1": {
      "decision": "excluded_noise",
      "reason": "Accessory verified from Listing"
    }
  }
}
```

Brand lists may support a decision but must not become the sole decision rule. Store every override and its evidence in the project scope rather than in the skill's global defaults.

## 6. Detail-Coverage Gate

The standard export may contain a much wider discovery pool than the selected detailed export. Apply this gate before market calculations:

- Keep all candidates in `candidate_manifest.csv`, including exclusions and missing-detail candidates.
- Resolve missing parent ASINs in the detailed export with the standard export's child-to-parent mapping.
- Only a candidate accepted into the current market layer and covered by the detailed export may enter sales, sales amount, parent count, share, annual trend, or rank denominators.
- Put accepted ASINs without detail coverage into a separate pending-collection list; do not write their metrics as zero.
- Use `target_child_asins.txt` as the auditable submission set for detailed collection.

This prevents a broad standard-export candidate list from inflating the measured market while retaining discovery evidence for later collection.

## 7. Layered Normalization And BI

Normalize `core_direct` and `adjacent_substitute` separately. Do not combine their sales into one unnamed market total.

For each layer:

1. Pass the audited candidate manifest to `normalize_sellersprite_exports.py` with the corresponding `--include-decisions` value.
2. Deduplicate at parent ASIN level; sibling child histories are not summed.
3. Keep SellerSprite sales amount separate from modeled GMV.
4. Calculate complete-year, YTD, and same-month-set comparisons only from available completed months.
5. Build brand competition from parent-deduplicated SellerSprite sales amount when that sheet exists.
6. Present product-attribute filters for form factor, storage, compatible devices, transcription offer/plan, dimensions/weight, bundle status, use case, and market layer where the evidence is available.
7. Show coverage counts: keyword rows, discovered children, accepted/detail-covered children, included parents, adjacent parents, exclusions, and review rows.

The dashboard title and scope note should describe the result as a query-based direct-competitor sample unless a separate, validated category baseline has been collected. It must not label the sample as total `AI Voice Recorder` TAM.

## 8. Acceptance Checks

The worked method is complete when:

- `keyword_evidence.csv` exposes the keyword clusters and original evidence.
- `candidate_manifest.csv` keeps every candidate, decision, reason, source, attribute evidence, and detail-coverage state.
- `parent_scope_manifest.csv` reconciles children to parents and keeps core/adjacent/excluded/review layers distinct.
- Every ASIN in sales totals has detailed-export coverage.
- Missing detail parents are reconciled from the standard child-to-parent map or left explicitly unresolved.
- Core and adjacent normalization totals reconcile independently to their accepted manifests.
- The HTML supports relevant Listing-attribute filters and states the sample limitation near the market scope.
- The final conclusions distinguish observed SellerSprite estimates, calculations, modeled metrics, inference, and unavailable values.

## 9. Reuse In Other Categories

Reuse the sequence, evidence model, four-layer decision, coverage gate, parent deduplication, and BI disclosure pattern. Replace all category-specific job definitions, keywords, attributes, brands, and exclusions with evidence from the new project. Never treat this example's recorder-specific taxonomy as a global rule.
