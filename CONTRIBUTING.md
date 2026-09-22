# Contributing

Contributions are welcome for public export adapters, scope manifests, parent-ASIN rules, synthetic fixtures, dashboard usability, documentation, and release validation.

## Before opening an issue or pull request

1. Use a synthetic or fully sanitized SellerSprite export.
2. Remove credentials, cookies, customer data, supplier identities, confidential ASIN lists, and local absolute paths.
3. State the marketplace, product task, cutoff date, export types, and expected evidence coverage.
4. Explain how the change was tested and whether it changes the market boundary or calculation denominator.

## Pull requests

Keep changes focused. Run the relevant tests:

```bash
python -m unittest discover -s sellersprite-bi-market-research/scripts -p "test_*.py" -v
```

Do not silently add child ASINs to a parent-level denominator, fill missing history with zero, or present SellerSprite estimates as Amazon settlement data. Do not add hidden tracking or credentials.

## Releases

Release manifests and provenance signatures are maintained by the publisher. Do not hand-edit signed release files in a feature pull request.
