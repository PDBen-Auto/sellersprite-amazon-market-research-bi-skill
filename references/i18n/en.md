# SellerSprite market research and BI

`sellersprite-bi-market-research` · English

## Purpose and scope

Expand seed intent to relevant ASINs, separate market layers and build auditable parent-deduplicated BI from SellerSprite exports.

## Implementation Basis and Dependencies

Defined market/product task, standard/detail XLSX and keyword exports as needed; Python 3 plus openpyxl for scripts. Online collection needs an authorized SellerSprite account/browser. Estimates are not Amazon settlement data.

## Inputs

Scope/date/marketplace and include/exclude rules; seed_keyword/seed_asins for discovery; conditional keyword, standard and detailed exports. Optional project relevance rules, attribute needs and output destinations. Never include credentials.

## Outputs

Candidate manifest with reasons and detailed coverage; parent/month/year/YTD/same-period, brand-revenue and rank-momentum datasets; self-contained dashboard.html, audit and missing-data records.

## Workflow

1. Freeze product task and scope.
2. Cluster keywords
3. classify core_direct, adjacent_substitute, excluded_noise and review.
4. Review uncertain/high-value exclusions.
5. Limit sales denominator to accepted detailed-covered products.
6. Deduplicate parent/month without summing siblings.
7. Separate units, revenue, modeled GMV and comparable month sets.
8. Keep global sample ranking fixed, momentum separate from opportunity.
9. Reconcile and test filters, images and pagination.

## Boundaries and stopping conditions

Search samples are not category TAM. Missing detailed exports stop historical claims; missing revenue yields N/A for brand-revenue/rank conclusions. Unknown is not zero. Keep US/CA/MX separate. No access bypass; ranking is sample revenue rank, not Amazon BSR.

## Example request

Use `$sellersprite-bi-market-research` — From keyword and competitor exports, create a scoped direct-market dashboard without including uncovered candidates in its sales denominator; respond in English and preserve evidence, unknowns and action boundaries.

## Complete specification

[Skill entrypoint and detailed references](../../SKILL.md).

Use the user's explicitly requested output language; otherwise follow the request language. Keep commands, skill IDs, JSON keys, enum values, units and source quotations unchanged. Separate translations from originals. Never infer country, currency or jurisdiction from language. Read the relevant detailed references in the complete specification and retain all existing validation and authorization gates.

Before delivery reconcile inputs, evidence, missing values, files and the original completion criteria. Mark unexecuted steps unverified; a successful script exit is not business validation.

## Language coverage and validation

This localized operating guide covers purpose, prerequisites, inputs, outputs, workflow, examples and boundaries; it is not a line-by-line translation of every reference. Detailed technical references, historical cases, script errors, example interfaces and images retain their original language. The assistant can explain them in the requested language. Structural, link and key-constraint checks are performed; native-speaker editorial review for each language is not claimed.

