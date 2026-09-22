# SellerSprite Amazon Market Research BI Skill

[![Release](https://img.shields.io/github/v/release/PDBen-Auto/sellersprite-amazon-market-research-bi-skill?display_name=tag&style=flat-square)](https://github.com/PDBen-Auto/sellersprite-amazon-market-research-bi-skill/releases/latest)
[![Validation](https://img.shields.io/github/actions/workflow/status/PDBen-Auto/sellersprite-amazon-market-research-bi-skill/validate.yml?branch=main&style=flat-square&label=validation)](https://github.com/PDBen-Auto/sellersprite-amazon-market-research-bi-skill/actions/workflows/validate.yml)
[![skills.sh](https://skills.sh/b/PDBen-Auto/sellersprite-amazon-market-research-bi-skill)](https://skills.sh/PDBen-Auto/sellersprite-amazon-market-research-bi-skill/sellersprite-bi-market-research)

An installable Agent Skill for auditable Amazon market research from SellerSprite exports.

It connects:

```text
keyword expansion -> similar-product discovery -> Listing filtering
-> candidate audit -> parent-ASIN deduplication -> interactive BI dashboard
```

The core question is not “can we draw a chart?” It is “which products actually belong to the market we are sizing, and can every inclusion be explained?”

## What it solves

Amazon category research can overstate opportunity when it mixes accessories, bundles, substitutes, unrelated listings, child ASINs, and inconsistent export coverage. This Skill creates an explicit market boundary before calculating competition or opportunity.

It preserves:

- keyword and competitor evidence;
- inclusion, exclusion, and review decisions for every candidate;
- Listing attributes used in relevance decisions;
- parent-ASIN deduplication rules;
- missing historical coverage and data conflicts;
- separate SellerSprite estimates, simulated GMV, and rank momentum calculations.

## Why it is different

| Common workflow | This Skill |
| --- | --- |
| Start with one broad keyword | Expand keyword intent and competitor evidence first |
| Treat every search result as part of the market | Classify candidates as `core_direct`, `adjacent_substitute`, `excluded_noise`, or `review` |
| Add every child ASIN to the denominator | Deduplicate to parent ASINs before market calculations |
| Fill missing history with zero | Preserve missing coverage and report a reduced result |
| Produce a chart with no audit trail | Retain candidate evidence, decision reasons, conflicts, and scope manifests |

## Install

```bash
npx skills add PDBen-Auto/sellersprite-amazon-market-research-bi-skill --skill sellersprite-bi-market-research
```

For a manual Codex installation:

```bash
git clone https://github.com/PDBen-Auto/sellersprite-amazon-market-research-bi-skill.git
cp -R sellersprite-amazon-market-research-bi-skill/sellersprite-bi-market-research ~/.codex/skills/sellersprite-bi-market-research
python -m pip install -r sellersprite-amazon-market-research-bi-skill/requirements.txt
```

The Release ZIP uses a flat layout. After extraction, the root `SKILL.md` is the discoverable entrypoint; the nested implementation directory is retained for compatibility with older manual installs.

## Use it when

- you have SellerSprite keyword-mining, competitor-standard, or detailed XLSX exports;
- you need Amazon FBA product research or competitor analysis with a defined market scope;
- you need keyword-to-ASIN discovery and Listing attribute filtering;
- you need parent-ASIN deduplication before sales or share calculations;
- you need a portable HTML BI dashboard that opens locally without a server.

Do not use it for listing copy, personal shopping recommendations, or a simple chart without a defined product task and market boundary.

## Example request

```text
Use $sellersprite-bi-market-research.
Marketplace: Amazon US
Seed keyword: ai voice recorder
Core competitor ASIN: B0FYQ4Y2ZZ

Expand relevant keywords and similar products, filter candidates by
transcription, summarization, subscription, form factor, and bundle
attributes, then use the SellerSprite standard and detailed exports to
produce an auditable BI dashboard.
```

## Outputs

- `keyword_evidence.csv` for keyword clusters and discovery evidence;
- `candidate_manifest.csv` for every candidate ASIN, decision, reason, and source;
- `parent_scope_manifest.csv` for the accepted parent-ASIN market boundary;
- normalized monthly, annual, YTD, same-period, brand-sales, and rank-momentum datasets;
- `conflicts.csv` for child-to-parent and historical-value conflicts;
- a self-contained `dashboard.html` that opens with `file://`.

## Worked case

The repository includes an AI Voice Recorder case covering Amazon US keyword expansion, direct versus adjacent market separation, Listing attribute filtering, parent-ASIN deduplication, and a final BI dashboard.

- [Live dashboard](https://pdben-auto.github.io/sellersprite-amazon-market-research-bi-skill/)
- [Worked example](sellersprite-bi-market-research/references/worked-example-ai-voice-recorder.md)
- [Discovery and relevance workflow](sellersprite-bi-market-research/references/discovery-and-relevance-workflow.md)

## Implementation basis and dependencies

The workflow relies on Python 3.10+, `openpyxl`, SellerSprite XLSX exports, a defined marketplace and product task, and the bundled normalization scripts. SellerSprite credentials are not stored in the repository or written into outputs.

- Missing keyword exports reduce discovery coverage.
- Missing detailed exports reduce the result to a current snapshot.
- An unresolved market boundary stops capacity conclusions.
- SellerSprite values are third-party estimates, not Amazon settlement data.

## Validation

```bash
python -m unittest discover -s sellersprite-bi-market-research/scripts -p "test_*.py" -v
```

The test suite covers keyword clustering, candidate layering, parent-ASIN deduplication, sales and rank calculations, missing sales fields, and scope filtering.

## Related PDBen-Auto Skills

- [Amazon Review Intelligence](https://github.com/PDBen-Auto/amazon-review-intelligence-skill) — written-review collection, evidence delivery, and VOC analysis.
- [Design Patent Search And Design Around](https://github.com/PDBen-Auto/design-patent-design-around-skill) — design-rights pre-screening and structurally distinct redesign planning.
- [Amazon Product Decision Gateway](https://github.com/PDBen-Auto/amazon-product-decision-suite) — cross-functional product validation and Go/No-Go handoff.

## Search terms

SellerSprite, Amazon market research, Amazon product research, Amazon FBA, keyword research, ASIN research, competitor analysis, similar product discovery, Listing attribute filtering, parent-ASIN deduplication, Amazon BI dashboard, e-commerce analytics, product opportunity analysis, Codex Skills, Agent Skills.

## Disclaimer

This project is not affiliated with SellerSprite or Amazon. Users are responsible for lawful access to source data and compliance with platform terms. Design and product decisions require appropriate human review.
