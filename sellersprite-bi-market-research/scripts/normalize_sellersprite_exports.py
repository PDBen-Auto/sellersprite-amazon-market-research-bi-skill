#!/usr/bin/env python3
"""Normalize SellerSprite standard/detail exports into BI-ready parent-level data."""

from __future__ import annotations

import argparse
import csv
import json
import math
import re
import statistics
from collections import Counter, defaultdict
from datetime import date, datetime
from pathlib import Path
from typing import Any, Iterable

import openpyxl


ASIN_RE = re.compile(r"^[A-Z0-9]{10}$", re.IGNORECASE)
MONTH_RE = re.compile(r"^(\d{4})-(\d{2})(?:\(\$\))?$")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--detail", required=True, help="SellerSprite Export details XLSX")
    parser.add_argument("--standard", help="SellerSprite standard Export XLSX")
    parser.add_argument(
        "--scope-manifest",
        help="Optional discovery manifest CSV with child_asin/parent_asin and decision columns",
    )
    parser.add_argument(
        "--include-decisions",
        default="core_direct",
        help="Comma-separated scope-manifest decisions to include (default: core_direct)",
    )
    parser.add_argument("--output-dir", required=True, help="Directory for normalized files")
    parser.add_argument("--as-of", default=date.today().isoformat(), help="Data cutoff, YYYY-MM-DD")
    parser.add_argument("--market-name", default="SellerSprite direct market")
    parser.add_argument("--marketplace", default="Amazon US")
    parser.add_argument("--currency", default="USD")
    parser.add_argument(
        "--rank-window-months",
        type=int,
        default=3,
        help="Months in each prior/recent global sales-rank window (default: 3)",
    )
    return parser.parse_args()


def as_number(value: Any) -> float | None:
    if value is None or isinstance(value, bool):
        return None
    if isinstance(value, (int, float)):
        if isinstance(value, float) and math.isnan(value):
            return None
        return float(value)
    text = str(value).strip().replace(",", "").replace("$", "")
    if not text:
        return None
    try:
        return float(text)
    except ValueError:
        return None


def safe_cell(row: tuple[Any, ...], index: int) -> Any:
    return row[index] if index < len(row) else None


def asin_values(values: Iterable[Any]) -> list[str]:
    found: list[str] = []
    for value in values:
        text = str(value).strip().upper() if value is not None else ""
        if ASIN_RE.fullmatch(text):
            found.append(text)
    return found


def month_key(value: Any) -> str | None:
    text = str(value).strip() if value is not None else ""
    match = MONTH_RE.fullmatch(text)
    if not match:
        return None
    return f"{match.group(1)}-{match.group(2)}"


def last_completed_month(as_of: date) -> str:
    year = as_of.year
    month = as_of.month - 1
    if month == 0:
        year -= 1
        month = 12
    return f"{year:04d}-{month:02d}"


def locate_header(sheet: Any) -> tuple[int, list[Any], dict[int, str]]:
    best: tuple[int, list[Any], dict[int, str]] | None = None
    max_row = min(sheet.max_row, 8)
    for row_index, row in enumerate(sheet.iter_rows(min_row=1, max_row=max_row, values_only=True), 1):
        header = list(row)
        months = {index: month for index, value in enumerate(header) if (month := month_key(value))}
        if months and (best is None or len(months) > len(best[2])):
            best = (row_index, header, months)
    if best is None:
        raise ValueError(f"No YYYY-MM columns found in sheet: {sheet.title}")
    return best


def classify_detail_sheets(workbook: openpyxl.Workbook) -> tuple[Any, Any | None, Any | None]:
    candidates: list[tuple[Any, list[Any], dict[int, str]]] = []
    for sheet in workbook.worksheets:
        try:
            _, header, months = locate_header(sheet)
        except ValueError:
            continue
        candidates.append((sheet, header, months))
    if not candidates:
        raise ValueError("No monthly data sheets found in detailed export")

    non_dollar = [item for item in candidates if not any("($)" in str(item[1][index]) for index in item[2])]
    dollar = [item for item in candidates if any("($)" in str(item[1][index]) for index in item[2])]

    def title_matches(item: tuple[Any, list[Any], dict[int, str]], terms: tuple[str, ...]) -> bool:
        title = item[0].title.casefold()
        return any(term.casefold() in title for term in terms)

    units_named = next(
        (
            item
            for item in non_dollar
            if title_matches(item, ("sales", "units", "销量", "月销量"))
        ),
        None,
    )
    revenue_named = next(
        (
            item
            for item in dollar
            if title_matches(item, ("sales amount", "revenue", "销售额", "销售金额"))
        ),
        None,
    )
    price_named = next(
        (
            item
            for item in dollar
            if title_matches(item, ("price", "价格", "售价"))
        ),
        None,
    )
    units_sheet = units_named[0] if units_named else (non_dollar[0][0] if non_dollar else candidates[0][0])
    revenue_sheet = revenue_named[0] if revenue_named else (dollar[0][0] if len(dollar) >= 2 else None)
    price_sheet = price_named[0] if price_named else (dollar[-1][0] if len(dollar) >= 2 else None)
    return units_sheet, revenue_sheet, price_sheet


def extract_monthly_records(sheet: Any, cutoff: str) -> tuple[list[dict[str, Any]], list[str]]:
    header_row, _, month_columns = locate_header(sheet)
    allowed_columns = {index: month for index, month in month_columns.items() if month <= cutoff}
    months = sorted(set(allowed_columns.values()))
    records: list[dict[str, Any]] = []
    for row in sheet.iter_rows(min_row=header_row + 1, values_only=True):
        ids = asin_values(row[:7])
        if not ids:
            continue
        child = ids[0]
        parent = ids[-1] if len(ids) > 1 else child
        url = next(
            (str(value).strip() for value in row[:8] if isinstance(value, str) and "amazon.com/" in value),
            "",
        )
        title = str(safe_cell(row, 5) or "").strip()
        values = {month: as_number(safe_cell(row, index)) for index, month in allowed_columns.items()}
        records.append(
            {
                "child_asin": child,
                "parent_asin": parent,
                "url": url,
                "title": title,
                "values": values,
            }
        )
    return records, months


def standard_records(path: Path) -> list[dict[str, Any]]:
    workbook = openpyxl.load_workbook(path, read_only=True, data_only=True)
    sheet = next((candidate for candidate in workbook.worksheets if candidate.max_column >= 30), workbook.worksheets[0])
    records: list[dict[str, Any]] = []
    for row in sheet.iter_rows(min_row=2, values_only=True):
        child = str(safe_cell(row, 0) or "").strip().upper()
        if not ASIN_RE.fullmatch(child):
            continue
        parent_raw = str(safe_cell(row, 8) or "").strip().upper()
        parent = parent_raw if ASIN_RE.fullmatch(parent_raw) else child
        launch = safe_cell(row, 34)
        if isinstance(launch, (datetime, date)):
            launch = launch.isoformat()[:10]
        records.append(
            {
                "child_asin": child,
                "parent_asin": parent,
                "sku": str(safe_cell(row, 1) or "").strip(),
                "attributes_raw": str(safe_cell(row, 2) or "").strip(),
                "brand": str(safe_cell(row, 3) or "Unknown").strip() or "Unknown",
                "title": str(safe_cell(row, 5) or "").strip(),
                "url": str(safe_cell(row, 6) or f"https://www.amazon.com/dp/{child}").strip(),
                "image": str(safe_cell(row, 7) or "").strip(),
                "current_units": as_number(safe_cell(row, 16)),
                "current_revenue": as_number(safe_cell(row, 19)),
                "price": as_number(safe_cell(row, 23)),
                "reviews": as_number(safe_cell(row, 27)),
                "rating": as_number(safe_cell(row, 29)),
                "fba_fee": as_number(safe_cell(row, 31)),
                "launch_date": str(launch or "").strip(),
                "fulfillment": str(safe_cell(row, 36) or "").strip(),
                "category": str(safe_cell(row, 9) or "").strip(),
                "leaf_category": str(safe_cell(row, 14) or "").strip(),
                "product_weight": str(safe_cell(row, 56) or safe_cell(row, 55) or "").strip(),
                "product_dimensions": str(safe_cell(row, 58) or safe_cell(row, 57) or "").strip(),
                "package_weight": str(safe_cell(row, 60) or safe_cell(row, 59) or "").strip(),
            }
        )
    return records


def load_scope_manifest(
    path: Path, include_decisions: set[str]
) -> tuple[set[str], set[str], dict[str, dict[str, Any]]]:
    children: set[str] = set()
    parents: set[str] = set()
    parent_attributes: dict[str, dict[str, Any]] = {}
    with path.open(encoding="utf-8-sig", newline="") as handle:
        for row in csv.DictReader(handle):
            decision = str(row.get("decision") or row.get("market_layer") or "").strip().casefold()
            if decision not in include_decisions:
                continue
            child = str(row.get("child_asin") or "").strip().upper()
            parent = str(row.get("parent_asin") or "").strip().upper()
            if ASIN_RE.fullmatch(child):
                children.add(child)
            if ASIN_RE.fullmatch(parent):
                parents.add(parent)
                parent_attributes[parent] = {
                    "market_layer": decision,
                    "relevance_score": as_number(row.get("relevance_score")),
                    "decision_reason": str(row.get("decision_reason") or "").strip(),
                }
    if not children and not parents:
        raise ValueError("Scope manifest contains no included child or parent ASINs")
    return children, parents, parent_attributes


def filter_records(
    records: list[dict[str, Any]], children: set[str], parents: set[str]
) -> list[dict[str, Any]]:
    return [
        record
        for record in records
        if record["child_asin"] in children or record["parent_asin"] in parents
    ]


def reconcile_parent_ids(
    records: list[dict[str, Any]], standard: list[dict[str, Any]]
) -> int:
    standard_parents = {
        record["child_asin"]: record["parent_asin"] for record in standard
    }
    changed = 0
    for record in records:
        standard_parent = standard_parents.get(record["child_asin"])
        if standard_parent and standard_parent != record["parent_asin"]:
            record["parent_asin"] = standard_parent
            changed += 1
    return changed


def choose_parent_month_values(
    records: list[dict[str, Any]], months: list[str]
) -> tuple[dict[str, dict[str, float]], list[dict[str, Any]]]:
    grouped: dict[tuple[str, str], list[tuple[str, float]]] = defaultdict(list)
    for record in records:
        for month in months:
            value = record["values"].get(month)
            if value is not None:
                grouped[(record["parent_asin"], month)].append((record["child_asin"], value))

    series: dict[str, dict[str, float]] = defaultdict(dict)
    conflicts: list[dict[str, Any]] = []
    for (parent, month), child_values in grouped.items():
        unique = sorted({round(value, 6) for _, value in child_values})
        selected = max(value for _, value in child_values)
        series[parent][month] = selected
        if len(unique) > 1:
            conflicts.append(
                {
                    "parent_asin": parent,
                    "month": month,
                    "selected": selected,
                    "child_values": [
                        {"child_asin": child, "value": value} for child, value in child_values
                    ],
                }
            )
    return dict(series), conflicts


def median_or_none(values: Iterable[float | None]) -> float | None:
    cleaned = [float(value) for value in values if value is not None and value > 0]
    return statistics.median(cleaned) if cleaned else None


def parent_metadata(
    standard: list[dict[str, Any]], detail: list[dict[str, Any]]
) -> dict[str, dict[str, Any]]:
    by_parent: dict[str, dict[str, Any]] = defaultdict(
        lambda: {"children": set(), "standard_rows": [], "titles": [], "urls": []}
    )
    for record in detail:
        parent = record["parent_asin"]
        by_parent[parent]["children"].add(record["child_asin"])
        if record["title"]:
            by_parent[parent]["titles"].append(record["title"])
        if record["url"]:
            by_parent[parent]["urls"].append(record["url"])
    for record in standard:
        parent = record["parent_asin"]
        by_parent[parent]["children"].add(record["child_asin"])
        by_parent[parent]["standard_rows"].append(record)
        if record["title"]:
            by_parent[parent]["titles"].append(record["title"])
        if record["url"]:
            by_parent[parent]["urls"].append(record["url"])

    result: dict[str, dict[str, Any]] = {}
    for parent, raw in by_parent.items():
        rows = raw["standard_rows"]
        brands = Counter(row["brand"] for row in rows if row["brand"])
        representative = max(
            rows,
            key=lambda row: (row.get("current_units") or -1, row.get("reviews") or -1),
            default={},
        )
        result[parent] = {
            "parent_asin": parent,
            "children": sorted(raw["children"]),
            "brand": brands.most_common(1)[0][0] if brands else "Unknown",
            "title": max(raw["titles"], key=len, default=""),
            "url": representative.get("url")
            or (raw["urls"][0] if raw["urls"] else f"https://www.amazon.com/dp/{parent}"),
            "image": representative.get("image", ""),
            "current_snapshot_units": max(
                (row["current_units"] for row in rows if row["current_units"] is not None),
                default=None,
            ),
            "standard_price": median_or_none(row["price"] for row in rows),
            "rating": max((row["rating"] for row in rows if row["rating"] is not None), default=None),
            "reviews": max((row["reviews"] for row in rows if row["reviews"] is not None), default=None),
            "fba_fee": median_or_none(row["fba_fee"] for row in rows),
            "launch_date": min((row["launch_date"] for row in rows if row["launch_date"]), default=""),
            "fulfillment": representative.get("fulfillment", ""),
            "category": representative.get("category", ""),
            "leaf_category": representative.get("leaf_category", ""),
            "sku": representative.get("sku", ""),
            "attributes_raw": representative.get("attributes_raw", ""),
            "product_weight": representative.get("product_weight", ""),
            "product_dimensions": representative.get("product_dimensions", ""),
            "package_weight": representative.get("package_weight", ""),
            "market_layer": "",
            "relevance_score": None,
            "decision_reason": "",
        }
    return result


def representative_prices(
    price_records: list[dict[str, Any]], metadata: dict[str, dict[str, Any]]
) -> dict[str, float | None]:
    values: dict[str, list[float]] = defaultdict(list)
    for record in price_records:
        values[record["parent_asin"]].extend(
            value for value in record["values"].values() if value is not None and value > 0
        )
    return {
        parent: median_or_none(values.get(parent, [])) or metadata[parent].get("standard_price")
        for parent in metadata
    }


def pct_growth(current: float, prior: float) -> float | None:
    return ((current / prior) - 1) * 100 if prior else None


def concentration(shares: list[float]) -> dict[str, float]:
    ordered = sorted(shares, reverse=True)
    return {
        "cr3": sum(ordered[:3]) * 100,
        "cr5": sum(ordered[:5]) * 100,
        "hhi": sum((share * 100) ** 2 for share in ordered),
    }


def competition_ranks(values: dict[str, float]) -> dict[str, int]:
    """Return descending competition ranks with stable parent-ASIN tie breaking."""
    ordered = sorted(values.items(), key=lambda item: (-item[1], item[0]))
    ranks: dict[str, int] = {}
    previous_value: float | None = None
    current_rank = 0
    for index, (parent, value) in enumerate(ordered, 1):
        if previous_value is None or value != previous_value:
            current_rank = index
        ranks[parent] = current_rank
        previous_value = value
    return ranks


def rank_momentum_rows(
    sales_amount_series: dict[str, dict[str, float]],
    months: list[str],
    metadata: dict[str, dict[str, Any]],
    window_months: int,
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    if window_months < 1:
        raise ValueError("--rank-window-months must be at least 1")

    observed_months = sorted(
        month
        for month in months
        if any(month in values for values in sales_amount_series.values())
    )
    required_count = window_months * 2
    if len(observed_months) < required_count:
        return (
            {
                "available": False,
                "metric": "SellerSprite parent-deduplicated sales amount",
                "window_months": window_months,
                "prior_months": [],
                "recent_months": [],
                "global_denominator": 0,
                "reason": f"At least {required_count} completed sales-amount months are required.",
            },
            [],
        )

    required_months = observed_months[-required_count:]
    prior_months = required_months[:window_months]
    recent_months = required_months[window_months:]
    complete_parents = {
        parent: values
        for parent, values in sales_amount_series.items()
        if all(month in values for month in required_months)
    }
    prior_values = {
        parent: sum(values[month] for month in prior_months)
        for parent, values in complete_parents.items()
    }
    recent_values = {
        parent: sum(values[month] for month in recent_months)
        for parent, values in complete_parents.items()
    }
    prior_ranks = competition_ranks(prior_values)
    recent_ranks = competition_ranks(recent_values)
    rows: list[dict[str, Any]] = []
    for parent in complete_parents:
        row = dict(metadata.get(parent, empty_metadata(parent)))
        row.update(
            {
                "prior_months": prior_months,
                "recent_months": recent_months,
                "prior_sales_amount": prior_values[parent],
                "recent_sales_amount": recent_values[parent],
                "prior_rank": prior_ranks[parent],
                "recent_rank": recent_ranks[parent],
                "rank_change": prior_ranks[parent] - recent_ranks[parent],
                "sales_amount_change": recent_values[parent] - prior_values[parent],
                "sales_amount_yoy": pct_growth(recent_values[parent], prior_values[parent]),
                "global_denominator": len(complete_parents),
            }
        )
        rows.append(row)
    rows.sort(key=lambda row: (row["recent_rank"], row["parent_asin"]))
    return (
        {
            "available": True,
            "metric": "SellerSprite parent-deduplicated sales amount",
            "window_months": window_months,
            "prior_months": prior_months,
            "recent_months": recent_months,
            "global_denominator": len(complete_parents),
            "positive_means": "Prior global rank minus recent global rank; positive means improvement.",
            "missing_rule": "A parent missing any required month is excluded; an observed zero is retained.",
            "filter_rule": "Dashboard filters may hide rows but must not recompute this denominator or ranks.",
            "label": "Calculated sample sales-amount rank; not Amazon BSR.",
        },
        rows,
    )


def empty_metadata(parent: str) -> dict[str, Any]:
    return {
        "parent_asin": parent,
        "children": [],
        "brand": "Unknown",
        "title": "",
        "url": f"https://www.amazon.com/dp/{parent}",
        "image": "",
        "current_snapshot_units": None,
        "standard_price": None,
        "rating": None,
        "reviews": None,
        "fba_fee": None,
        "launch_date": "",
        "fulfillment": "",
        "category": "",
        "leaf_category": "",
        "sku": "",
        "attributes_raw": "",
        "product_weight": "",
        "product_dimensions": "",
        "package_weight": "",
        "market_layer": "",
        "relevance_score": None,
        "decision_reason": "",
    }


def build_payload(args: argparse.Namespace) -> dict[str, Any]:
    as_of = date.fromisoformat(args.as_of)
    cutoff = last_completed_month(as_of)
    detail_path = Path(args.detail).resolve()
    standard_path = Path(args.standard).resolve() if args.standard else None
    workbook = openpyxl.load_workbook(detail_path, read_only=True, data_only=True)
    units_sheet, revenue_sheet, price_sheet = classify_detail_sheets(workbook)
    unit_records, months = extract_monthly_records(units_sheet, cutoff)
    revenue_records, revenue_months = (
        extract_monthly_records(revenue_sheet, cutoff) if revenue_sheet else ([], [])
    )
    price_records, _ = extract_monthly_records(price_sheet, cutoff) if price_sheet else ([], [])
    standard = standard_records(standard_path) if standard_path else []
    scope_path = Path(args.scope_manifest).resolve() if args.scope_manifest else None
    scope_attributes: dict[str, dict[str, Any]] = {}
    if scope_path:
        include_decisions = {
            value.strip().casefold() for value in args.include_decisions.split(",") if value.strip()
        }
        if not include_decisions:
            raise ValueError("--include-decisions must contain at least one decision")
        scope_children, scope_parents, scope_attributes = load_scope_manifest(
            scope_path, include_decisions
        )
        unit_records = filter_records(unit_records, scope_children, scope_parents)
        revenue_records = filter_records(revenue_records, scope_children, scope_parents)
        price_records = filter_records(price_records, scope_children, scope_parents)

    detail_children = {record["child_asin"] for record in unit_records}
    detail_parents = {record["parent_asin"] for record in unit_records}
    standard = filter_records(standard, detail_children, detail_parents) if standard else []
    reconciled_children = reconcile_parent_ids(unit_records, standard)
    reconcile_parent_ids(revenue_records, standard)
    reconcile_parent_ids(price_records, standard)
    metadata = parent_metadata(standard, unit_records)
    for parent, attributes in scope_attributes.items():
        if parent in metadata:
            metadata[parent].update(attributes)
    unit_series, unit_conflicts = choose_parent_month_values(unit_records, months)
    sales_amount_series, sales_amount_conflicts = choose_parent_month_values(
        revenue_records, revenue_months
    )
    prices = representative_prices(price_records, metadata)

    all_parents = sorted(set(metadata) | set(unit_series) | set(sales_amount_series))
    for parent in all_parents:
        metadata.setdefault(parent, empty_metadata(parent))
        prices.setdefault(parent, metadata[parent].get("standard_price"))

    observed_months = sorted(
        {
            month
            for month in set(months) | set(revenue_months)
            if any(
                month in unit_series.get(parent, {})
                or month in sales_amount_series.get(parent, {})
                for parent in all_parents
            )
        }
    )
    parent_monthly: list[dict[str, Any]] = []
    for parent in all_parents:
        for month in observed_months:
            units = unit_series.get(parent, {}).get(month)
            sales_amount = sales_amount_series.get(parent, {}).get(month)
            price = prices.get(parent)
            modeled_gmv = units * price if units is not None and price is not None else None
            if units is None and sales_amount is None:
                continue
            parent_monthly.append(
                {
                    "parent_asin": parent,
                    "brand": metadata[parent]["brand"],
                    "title": metadata[parent]["title"],
                    "month": month,
                    "units": units,
                    "seller_sprite_sales_amount": sales_amount,
                    "representative_price": price,
                    "modeled_gmv": modeled_gmv,
                }
            )

    market_monthly: list[dict[str, Any]] = []
    for month in observed_months:
        observed_units = {
            parent: unit_series[parent][month]
            for parent in all_parents
            if month in unit_series.get(parent, {})
        }
        observed_sales_amount = {
            parent: sales_amount_series[parent][month]
            for parent in all_parents
            if month in sales_amount_series.get(parent, {})
        }
        units = sum(observed_units.values())
        seller_sprite_sales_amount = (
            sum(observed_sales_amount.values()) if observed_sales_amount else None
        )
        gmv = sum(
            value * prices[parent]
            for parent, value in observed_units.items()
            if prices.get(parent) is not None
        )
        market_monthly.append(
            {
                "month": month,
                "units": units,
                "seller_sprite_sales_amount": seller_sprite_sales_amount,
                "modeled_gmv": gmv,
                "active_parents": sum(1 for value in observed_units.values() if value > 0),
                "unit_parent_coverage": len(observed_units),
                "sales_amount_parent_coverage": len(observed_sales_amount),
            }
        )

    monthly_lookup = {row["month"]: row for row in market_monthly}
    for row in market_monthly:
        year, month = map(int, row["month"].split("-"))
        prior = monthly_lookup.get(f"{year - 1:04d}-{month:02d}")
        row["unit_yoy"] = pct_growth(row["units"], prior["units"]) if prior else None
        row["gmv_yoy"] = pct_growth(row["modeled_gmv"], prior["modeled_gmv"]) if prior else None
        row["sales_amount_yoy"] = (
            pct_growth(row["seller_sprite_sales_amount"], prior["seller_sprite_sales_amount"])
            if prior
            and row["seller_sprite_sales_amount"] is not None
            and prior["seller_sprite_sales_amount"] is not None
            else None
        )

    annual: list[dict[str, Any]] = []
    for year in sorted({int(month[:4]) for month in observed_months}):
        rows = [row for row in market_monthly if row["month"].startswith(f"{year:04d}-")]
        units = sum(row["units"] for row in rows)
        gmv = sum(row["modeled_gmv"] for row in rows)
        sales_amount_values = [
            row["seller_sprite_sales_amount"]
            for row in rows
            if row["seller_sprite_sales_amount"] is not None
        ]
        seller_sprite_sales_amount = (
            sum(sales_amount_values) if len(sales_amount_values) == len(rows) else None
        )
        active = {
            parent
            for parent in all_parents
            if any(unit_series.get(parent, {}).get(row["month"], 0) > 0 for row in rows)
        }
        annual.append(
            {
                "year": year,
                "months": [row["month"] for row in rows],
                "month_count": len(rows),
                "is_full_year": len(rows) == 12,
                "units": units,
                "seller_sprite_sales_amount": seller_sprite_sales_amount,
                "modeled_gmv": gmv,
                "sales_weighted_asp": (
                    seller_sprite_sales_amount / units
                    if seller_sprite_sales_amount is not None and units
                    else None
                ),
                "modeled_asp": gmv / units if units else None,
                "active_parents": len(active),
            }
        )

    latest_month = max(observed_months) if observed_months else None
    current_year = int(latest_month[:4]) if latest_month else as_of.year
    current_month_number = int(latest_month[5:7]) if latest_month else 0
    current_period = [f"{current_year:04d}-{month:02d}" for month in range(1, current_month_number + 1)]
    prior_period = [f"{current_year - 1:04d}-{month:02d}" for month in range(1, current_month_number + 1)]

    def sum_period(period: list[str], field: str) -> float:
        return sum(monthly_lookup.get(month, {}).get(field, 0.0) for month in period)

    current_units = sum_period(current_period, "units")
    prior_units = sum_period(prior_period, "units")
    current_gmv = sum_period(current_period, "modeled_gmv")
    prior_gmv = sum_period(prior_period, "modeled_gmv")
    current_sales_amount_values = [
        monthly_lookup.get(month, {}).get("seller_sprite_sales_amount") for month in current_period
    ]
    prior_sales_amount_values = [
        monthly_lookup.get(month, {}).get("seller_sprite_sales_amount") for month in prior_period
    ]
    current_sales_amount = (
        sum(current_sales_amount_values)
        if current_sales_amount_values and all(value is not None for value in current_sales_amount_values)
        else None
    )
    prior_sales_amount = (
        sum(prior_sales_amount_values)
        if prior_sales_amount_values and all(value is not None for value in prior_sales_amount_values)
        else None
    )
    same_period = {
        "current_year": current_year,
        "prior_year": current_year - 1,
        "months_compared": current_month_number,
        "current_units": current_units,
        "prior_units": prior_units,
        "unit_yoy": pct_growth(current_units, prior_units),
        "current_modeled_gmv": current_gmv,
        "prior_modeled_gmv": prior_gmv,
        "gmv_yoy": pct_growth(current_gmv, prior_gmv),
        "current_seller_sprite_sales_amount": current_sales_amount,
        "prior_seller_sprite_sales_amount": prior_sales_amount,
        "sales_amount_yoy": (
            pct_growth(current_sales_amount, prior_sales_amount)
            if current_sales_amount is not None and prior_sales_amount is not None
            else None
        ),
        "prior_coverage_complete": all(month in monthly_lookup for month in prior_period),
    }

    parent_current: list[dict[str, Any]] = []
    if latest_month:
        total_latest_units = monthly_lookup[latest_month]["units"]
        total_latest_gmv = monthly_lookup[latest_month]["modeled_gmv"]
        total_latest_sales_amount = monthly_lookup[latest_month]["seller_sprite_sales_amount"]
        for parent in all_parents:
            units = unit_series.get(parent, {}).get(latest_month, 0.0)
            sales_amount = sales_amount_series.get(parent, {}).get(latest_month)
            price = prices.get(parent)
            gmv = units * price if price is not None else 0.0
            row = dict(metadata[parent])
            row.update(
                {
                    "representative_price": price,
                    "latest_month": latest_month,
                    "units": units,
                    "seller_sprite_sales_amount": sales_amount,
                    "modeled_gmv": gmv,
                    "unit_share": units / total_latest_units if total_latest_units else 0.0,
                    "sales_amount_share": (
                        sales_amount / total_latest_sales_amount
                        if sales_amount is not None and total_latest_sales_amount
                        else None
                    ),
                    "gmv_share": gmv / total_latest_gmv if total_latest_gmv else 0.0,
                }
            )
            parent_current.append(row)
    parent_current.sort(
        key=lambda row: (
            -(row["seller_sprite_sales_amount"] or 0),
            -row["units"],
            row["parent_asin"],
        )
    )

    brand_units: dict[str, float] = defaultdict(float)
    brand_sales_amount: dict[str, float] = defaultdict(float)
    for row in parent_current:
        brand_units[row["brand"]] += row["units"]
        if row["seller_sprite_sales_amount"] is not None:
            brand_sales_amount[row["brand"]] += row["seller_sprite_sales_amount"]
    total_brand_units = sum(brand_units.values())
    total_brand_sales_amount = sum(brand_sales_amount.values())
    parent_unit_competition = concentration([row["unit_share"] for row in parent_current])
    brand_unit_competition = concentration(
        [units / total_brand_units for units in brand_units.values()]
    ) if total_brand_units else concentration([])
    parent_sales_amount_competition = (
        concentration(
            [
                row["seller_sprite_sales_amount"] / total_brand_sales_amount
                for row in parent_current
                if row["seller_sprite_sales_amount"] is not None
            ]
        )
        if total_brand_sales_amount
        else None
    )
    brand_sales_amount_competition = (
        concentration(
            [sales_amount / total_brand_sales_amount for sales_amount in brand_sales_amount.values()]
        )
        if total_brand_sales_amount
        else None
    )

    rank_summary, rank_rows = rank_momentum_rows(
        sales_amount_series,
        revenue_months,
        metadata,
        args.rank_window_months,
    )
    combined_conflicts = [
        {**conflict, "metric": "units"} for conflict in unit_conflicts
    ] + [
        {**conflict, "metric": "seller_sprite_sales_amount"}
        for conflict in sales_amount_conflicts
    ]
    warnings = [
        "SellerSprite values are third-party estimates, not Amazon settlement data.",
        "Standard export recent-sales snapshots and calendar-month detailed history have different time windows.",
        "The figures describe the submitted ASIN universe, not category TAM unless coverage is separately proven.",
    ]
    if not standard_path:
        warnings.append("Standard export was not supplied; brand/current metadata are incomplete.")
    if not revenue_sheet:
        warnings.append(
            "No SellerSprite sales-amount sheet was detected; sales-amount competition and rank momentum are N/A."
        )
    elif not rank_summary["available"]:
        warnings.append(rank_summary["reason"])

    return {
        "metadata": {
            "market_name": args.market_name,
            "marketplace": args.marketplace,
            "currency": args.currency,
            "as_of": args.as_of,
            "last_completed_month": cutoff,
            "latest_month_in_detail": latest_month,
            "standard_file": standard_path.name if standard_path else None,
            "detail_file": detail_path.name,
            "scope_manifest": scope_path.name if scope_path else None,
            "units_sheet": units_sheet.title,
            "revenue_sheet_detected": revenue_sheet.title if revenue_sheet else None,
            "price_sheet_detected": price_sheet.title if price_sheet else None,
            "input_child_rows": len(unit_records),
            "standard_child_rows": len(standard),
            "parent_ids_reconciled_from_standard": reconciled_children,
            "unique_parents": len(all_parents),
            "rank_window_months": args.rank_window_months,
        },
        "parent_monthly": parent_monthly,
        "market_monthly": market_monthly,
        "annual": annual,
        "same_period": same_period,
        "parent_current": parent_current,
        "competition": {
            "default_basis": "seller_sprite_sales_amount",
            "parent_sales_amount": parent_sales_amount_competition,
            "brand_sales_amount": brand_sales_amount_competition,
            "parent_units": parent_unit_competition,
            "brand_units": brand_unit_competition,
            "brands_by_sales_amount": [
                {
                    "brand": brand,
                    "seller_sprite_sales_amount": sales_amount,
                    "share": sales_amount / total_brand_sales_amount if total_brand_sales_amount else None,
                }
                for brand, sales_amount in sorted(
                    brand_sales_amount.items(), key=lambda item: item[1], reverse=True
                )
            ],
            "brands_by_units": [
                {
                    "brand": brand,
                    "units": units,
                    "share": units / total_brand_units if total_brand_units else 0.0,
                }
                for brand, units in sorted(brand_units.items(), key=lambda item: item[1], reverse=True)
            ],
        },
        "rank_momentum": {
            "summary": rank_summary,
            "rows": rank_rows,
        },
        "data_quality": {
            "parent_month_conflict_count": len(combined_conflicts),
            "unit_conflict_count": len(unit_conflicts),
            "sales_amount_conflict_count": len(sales_amount_conflicts),
            "conflicts": combined_conflicts,
            "gmv_method": "Deduplicated parent units multiplied by median observed historical parent price; standard price fallback.",
            "sales_amount_method": "SellerSprite sales amount deduplicated by parent ASIN and month; maximum visible sibling value selected on conflict.",
            "dedupe_method": "Group by parent ASIN and month; choose maximum visible sibling value when nonblank values conflict.",
            "in_progress_month_excluded": f"{as_of.year:04d}-{as_of.month:02d}",
            "warnings": warnings,
        },
    }


def write_csv(path: Path, fieldnames: list[str], rows: Iterable[dict[str, Any]]) -> None:
    with path.open("w", newline="", encoding="utf-8-sig") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    args = parse_args()
    output_dir = Path(args.output_dir).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    payload = build_payload(args)
    (output_dir / "dashboard_data.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    write_csv(
        output_dir / "market_monthly.csv",
        [
            "month",
            "units",
            "seller_sprite_sales_amount",
            "modeled_gmv",
            "active_parents",
            "unit_parent_coverage",
            "sales_amount_parent_coverage",
            "unit_yoy",
            "sales_amount_yoy",
            "gmv_yoy",
        ],
        payload["market_monthly"],
    )
    write_csv(
        output_dir / "parent_monthly.csv",
        [
            "parent_asin",
            "brand",
            "title",
            "month",
            "units",
            "seller_sprite_sales_amount",
            "representative_price",
            "modeled_gmv",
        ],
        payload["parent_monthly"],
    )
    write_csv(
        output_dir / "parent_current.csv",
        [
            "parent_asin",
            "children",
            "market_layer",
            "relevance_score",
            "decision_reason",
            "brand",
            "title",
            "url",
            "image",
            "category",
            "leaf_category",
            "sku",
            "attributes_raw",
            "product_weight",
            "product_dimensions",
            "package_weight",
            "representative_price",
            "rating",
            "reviews",
            "launch_date",
            "fulfillment",
            "latest_month",
            "units",
            "seller_sprite_sales_amount",
            "modeled_gmv",
            "unit_share",
            "sales_amount_share",
            "gmv_share",
        ],
        ({**row, "children": " ".join(row["children"])} for row in payload["parent_current"]),
    )
    conflict_rows = [
        {
            "parent_asin": conflict["parent_asin"],
            "month": conflict["month"],
            "metric": conflict["metric"],
            "selected": conflict["selected"],
            "child_values": json.dumps(conflict["child_values"], ensure_ascii=False),
        }
        for conflict in payload["data_quality"]["conflicts"]
    ]
    write_csv(
        output_dir / "conflicts.csv",
        ["parent_asin", "month", "metric", "selected", "child_values"],
        conflict_rows,
    )
    write_csv(
        output_dir / "rank_momentum.csv",
        [
            "parent_asin",
            "brand",
            "title",
            "url",
            "image",
            "prior_months",
            "recent_months",
            "prior_sales_amount",
            "recent_sales_amount",
            "prior_rank",
            "recent_rank",
            "rank_change",
            "sales_amount_change",
            "sales_amount_yoy",
            "global_denominator",
        ],
        (
            {
                **row,
                "prior_months": " ".join(row["prior_months"]),
                "recent_months": " ".join(row["recent_months"]),
            }
            for row in payload["rank_momentum"]["rows"]
        ),
    )
    metadata = payload["metadata"]
    print(
        f"Normalized {metadata['input_child_rows']} detailed child rows into "
        f"{metadata['unique_parents']} parents through {metadata['latest_month_in_detail']}; "
        f"conflicts={payload['data_quality']['parent_month_conflict_count']}; "
        f"rank_denominator={payload['rank_momentum']['summary']['global_denominator']}."
    )


if __name__ == "__main__":
    main()
