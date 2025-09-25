#!/usr/bin/env python3
"""Generate per-bank fixture files from catalog.yaml."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Any
import yaml

ROOT = Path(__file__).resolve().parent.parent
CATALOG = ROOT / "fixtures" / "catalog.yaml"
OUTPUT_DIR = ROOT / "fixtures"

DATE_FORMAT_MAP = {
    "YYYY-MM-DD": "%Y-%m-%d",
    "DD/MM/YYYY": "%d/%m/%Y",
    "DD.MM.YYYY": "%d.%m.%Y",
}


@dataclass
class SoftwareProfile:
    id: str
    name: str
    profile: str
    folder: str
    locale_overrides: Dict[str, str]

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "SoftwareProfile":
        return cls(
            id=data["id"],
            name=data["name"],
            profile=data["profile"],
            folder=data["folder"],
            locale_overrides=data.get("locale_overrides", {}),
        )

    def profile_for_region(self, region_code: str) -> str:
        return self.locale_overrides.get(region_code, self.profile)


def load_catalog() -> Dict[str, Any]:
    return yaml.safe_load(CATALOG.read_text())


def format_date(date_obj: datetime, pattern: str) -> str:
    try:
        strftime_pattern = DATE_FORMAT_MAP[pattern]
    except KeyError:
        raise ValueError(f"Unsupported date format pattern: {pattern}") from None
    return date_obj.strftime(strftime_pattern)


def format_amount(amount: float, decimal_separator: str) -> float:
    if decimal_separator == ",":
        # Represent as string with comma decimal for clarity in fixtures
        return float(f"{amount:.2f}")
    return round(amount, 2)


def generate_rows(bank: Dict[str, Any], region: Dict[str, Any], template: Dict[str, Any]) -> list[Dict[str, Any]]:
    rows = []
    start = datetime.fromisoformat(bank["statement_period"]["start"])
    balance = float(bank["opening_balance"])
    date_pattern = region["date_format"]
    decimal_sep = region["decimal_separator"]

    opening_row = {
        "unique_id": f"{bank['slug'].upper().replace('-', '')}-{start.strftime('%Y%m%d')}-000",
        "transaction_date": format_date(start, date_pattern),
        "description": "Opening balance",
        "debit_credit": "credit",
        "amount": 0.00,
        "balance": round(balance, 2),
        "memo": "Starting balance",
    }
    rows.append(opening_row)

    for index, txn in enumerate(template["transactions"], start=1):
        txn_date = start + timedelta(days=int(txn["days_from_start"]))
        amount = float(txn["amount"])
        debit_credit = txn["debit_credit"]
        if debit_credit == "credit":
            balance += amount
        else:
            balance -= amount

        unique = f"{bank['slug'].upper().replace('-', '')}-{txn_date.strftime('%Y%m%d')}-{index:03d}"
        row = {
            "unique_id": unique,
            "transaction_date": format_date(txn_date, date_pattern),
            "description": txn["description"],
            "debit_credit": debit_credit,
            "amount": round(amount, 2) if decimal_sep == "." else round(amount, 2),
            "balance": round(balance, 2),
            "memo": txn["memo"],
        }
        rows.append(row)

    return rows


def build_fixture(bank: Dict[str, Any], region: Dict[str, Any], softwares: list[SoftwareProfile], template: Dict[str, Any]) -> Dict[str, Any]:
    software_profiles = {}
    for software in softwares:
        software_profiles[software.id] = {
            "profile": software.profile_for_region(region["code"]),
            "folder": software.folder,
            "filename_suffix": f"{region['code'].lower()}-standard",
        }

    fixture = {
        "version": 1,
        "bank": {
            "name": bank["name"],
            "slug": bank["slug"],
        },
        "country": {
            "code": region["code"],
            "name": region["name"],
        },
        "currency": region["currency"],
        "locale": region["locale"],
        "date_format": region["date_format"],
        "decimal_separator": region["decimal_separator"],
        "thousands_separator": region["thousands_separator"],
        "account_type": bank["account_type"],
        "statement_period": bank["statement_period"],
        "opening_balance": round(float(bank["opening_balance"]), 2),
        "software_profiles": software_profiles,
        "rows": generate_rows(bank, region, template),
    }

    return fixture


def main() -> None:
    data = load_catalog()
    softwares = [SoftwareProfile.from_dict(item) for item in data["softwares"]]
    template = data["statement_template"]

    for region in data["regions"]:
        output_dir = OUTPUT_DIR / region["code"].lower()
        output_dir.mkdir(parents=True, exist_ok=True)
        for bank in region["banks"]:
            fixture = build_fixture(bank, region, softwares, template)
            target = output_dir / f"{bank['slug']}.yaml"
            target.write_text(yaml.safe_dump(fixture, sort_keys=False, allow_unicode=True))
            print(f"Generated {target.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
