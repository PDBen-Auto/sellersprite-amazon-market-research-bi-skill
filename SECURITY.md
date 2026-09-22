# Security Policy

## Supported surface

Report issues in export parsing, ASIN scope classification, parent-ASIN deduplication, dashboard generation, accidental data disclosure, or release-boundary checks.

SellerSprite values are third-party estimates. This repository does not store SellerSprite credentials and does not authorize access to data the user cannot lawfully access.

## Reporting

Use GitHub private vulnerability reporting when available. Otherwise contact the repository owner privately. Never include credentials, cookies, customer data, private exports, supplier records, or confidential product identifiers.

## Operational rules

- Reproduce with synthetic or fully sanitized XLSX/CSV/JSON fixtures.
- Treat missing detailed coverage as missing evidence, not zero sales.
- Treat unsigned or hash-mismatched releases as invalid.
- Do not add telemetry, hidden prompts, callbacks, or account-control bypasses.
