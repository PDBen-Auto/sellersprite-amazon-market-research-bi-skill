---
name: sellersprite-bi-market-research
description: Research an Amazon market from SellerSprite keyword and competitor exports, filter relevant ASINs by product task and listing attributes, deduplicate parent ASINs, and produce auditable category BI. Use for SellerSprite market research, Amazon FBA product research, keyword-to-ASIN discovery, competitor analysis, parent-ASIN deduplication, or interactive BI dashboards. Do not use for listing copy, personal shopping recommendations, or a simple chart without a defined market scope.
---

# SellerSprite Amazon Market Research BI

Use the full implementation guide in [sellersprite-bi-market-research/SKILL.md](sellersprite-bi-market-research/SKILL.md). The nested package is retained for backward-compatible manual installation; this root entrypoint makes the repository discoverable by Agent Skills directories and `npx skills add`.

## Implementation Basis And Dependencies

The workflow is based on SellerSprite keyword-mining, competitor-standard, and detailed XLSX exports; Python normalization scripts; parent-ASIN evidence rules; and a self-contained HTML dashboard. It is feasible when the user provides a defined marketplace and product task plus the relevant exports, or authorizes an online export workflow. `openpyxl` and Python 3 are required for the bundled scripts. Missing keyword exports reduce discovery coverage; missing detailed exports reduce the result to a snapshot; an undefined market boundary stops capacity conclusions. SellerSprite estimates remain third-party evidence, not Amazon settlement data.

## Inputs

- `scope_manifest` (required): marketplace, product task, inclusion/exclusion rules, and as-of date. Accept JSON, CSV, or Markdown; stop capacity conclusions when the boundary is unresolved.
- `seed_keyword` and `seed_asins` (required for discovery): the starting search intent and at least one valid ASIN. Validate marketplace and ASIN format before expansion.
- `keyword_export`, `standard_export`, and `detail_export` (conditional): SellerSprite XLSX files used for discovery, metadata, and historical BI. Preserve missing coverage as an explicit gap instead of filling it with zero.
- `discovery_rules` and `output_request` (optional): project-specific relevance rules and requested CSV/JSON/HTML destinations. Never include credentials or cookies.

## Outputs

- Auditable candidate and parent scope manifests with inclusion decisions, evidence, reasons, and detailed-export coverage.
- Parent-deduplicated monthly, annual, YTD, same-period, brand-sales, and rank-momentum datasets with conflicts and missing values preserved.
- A self-contained `dashboard.html` that opens with `file://`, plus quality and source notes.
- Partial results with explicit coverage gaps when an export, permission, network route, or browser capability is unavailable. No fictitious TAM, sales, or historical trend is generated.

## Workflow

1. Freeze the product task, marketplace, time boundary, and inclusion/exclusion rules.
2. Read the nested implementation guide and relevant references for discovery, data contract, collection, and dashboard standards.
3. Discover and classify candidates as `core_direct`, `adjacent_substitute`, `excluded_noise`, or `review`; retain exclusions for audit.
4. Normalize only accepted ASINs with detailed coverage into sales denominators, deduplicate by parent ASIN, and generate the requested BI artifacts.
5. Validate files, totals, scope, responsive HTML behavior, and trigger boundaries before reporting completion.

## Related Skills

- [Amazon Review Intelligence](https://github.com/PDBen-Auto/amazon-review-intelligence-skill)
- [Design Patent Search And Design Around](https://github.com/PDBen-Auto/design-patent-design-around-skill)
- [Amazon Product Decision Gateway](https://github.com/PDBen-Auto/amazon-product-decision-suite)
