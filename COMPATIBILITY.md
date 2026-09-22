# Compatibility

| Surface | Supported | Notes |
| --- | --- | --- |
| Codex / Agent Skills | Yes | Install with `npx skills add` or copy the Skill directory. |
| Python | 3.10+ | `openpyxl` is required for XLSX normalization. |
| Inputs | SellerSprite keyword, competitor-standard, and detailed XLSX exports | Existing sanitized JSON/CSV can be used for analysis-only workflows. |
| Output | CSV/JSON evidence, normalized datasets, standalone HTML BI | The dashboard opens locally without a server. |
| SellerSprite login | Conditional | Needed only for fresh online export collection; credentials are never stored. |
| Windows / Linux | Supported | Browser automation is optional and environment-dependent. |

Missing keyword or detailed exports reduce discovery or historical coverage. The Skill must label the reduction and must not fabricate market size or zero-fill missing sales history.
