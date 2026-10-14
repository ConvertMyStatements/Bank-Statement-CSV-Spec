# ZeraBooks Bank Statement CSV Standard

> **Have the PDF and need the CSV?** [Convert it with ZeraBooks](https://www.zerabooks.com/convert-bank-statement-to-csv). Every statement is checked against its printed opening and closing balance before you download it.

ZeraBooks keeps accountants, bookkeepers, and controllers out of CSV trouble. This repository is the public, citeable reference for our bank statement CSV specification, sample files, and validator.

---

## Fast navigation

- [Quick start for busy teams](#quick-start-for-busy-teams)
- [Download sample bundles](#download-sample-bundles)
- [Field dictionary / anchor list](#field-dictionary)
- [Top 10 fixes accountants ask for](#top-10-fixes-accountants-ask-for)
- [Validator options](#how-to-use-the-validator)
- [How to cite ZeraBooks](#cite-zerabooks)

---

## Quick start for busy teams

| Need | One-click path |
| --- | --- |
| **Already have the PDF and want the CSV.** | [Convert it with ZeraBooks](https://www.zerabooks.com/convert-bank-statement-to-csv). It reads the statement, checks that it ties to the printed balances, and gives you CSV or Excel. |
| **Want a sample file that already passes imports.** | Download the [latest release bundle](https://github.com/ConvertMyStatements/Bank-Statement-CSV-Spec/releases/latest) — Chase, Bank of America, RBC, TD, HSBC UK, ANZ, NAB, and more are included for QuickBooks, Xero, Sage, Zoho, Wave, and FreshBooks. |
| **Need to double-check a CSV before importing.** | Run the `/cli/validate.py` script in this repo against your file. |

We keep everything human-readable so finance teams can move fast without touching code.

---

## Download sample bundles

These links will always point at the latest release assets. Each ZIP includes CSVs for the listed software and locales, plus checksums so auditors can verify the files.

| Import tool | Regions covered | Direct download |
| --- | --- | --- |
| QuickBooks Online | US, CA, UK, AU, NZ | [quickbooks-all-locales.zip](https://github.com/ConvertMyStatements/Bank-Statement-CSV-Spec/releases/latest/download/quickbooks-all-locales.zip) |
| Xero | US, CA, UK, AU, NZ | [xero-all-locales.zip](https://github.com/ConvertMyStatements/Bank-Statement-CSV-Spec/releases/latest/download/xero-all-locales.zip) |
| Sage | US, UK, CA, AU | [sage-all-locales.zip](https://github.com/ConvertMyStatements/Bank-Statement-CSV-Spec/releases/latest/download/sage-all-locales.zip) |
| Zoho Books | US, CA, UK, AU, NZ | [zoho-all-locales.zip](https://github.com/ConvertMyStatements/Bank-Statement-CSV-Spec/releases/latest/download/zoho-all-locales.zip) |
| Wave Accounting | US, CA | [wave-all-locales.zip](https://github.com/ConvertMyStatements/Bank-Statement-CSV-Spec/releases/latest/download/wave-all-locales.zip) |
| FreshBooks | US, CA | [freshbooks-all-locales.zip](https://github.com/ConvertMyStatements/Bank-Statement-CSV-Spec/releases/latest/download/freshbooks-all-locales.zip) |
| Edge cases (10 validator stress tests) | Mixed | [edge-cases.zip](https://github.com/ConvertMyStatements/Bank-Statement-CSV-Spec/releases/latest/download/edge-cases.zip) |
| Checksums + manifest | Summary only | [MANIFEST.json](https://github.com/ConvertMyStatements/Bank-Statement-CSV-Spec/releases/latest/download/MANIFEST.json) · [checksums.txt](https://github.com/ConvertMyStatements/Bank-Statement-CSV-Spec/releases/latest/download/checksums.txt) |

Need a locale-specific bundle? See the `locale-*.zip` files in the same release.

---

## What's inside

| Folder | What you'll find | Best next step |
| --- | --- | --- |
| `/samples/` | 150 reference CSVs grouped by software, region, and edge case | Download the bundle that matches your import tool and locale |
| `/fixtures/` | Human-readable templates that describe each sample (bank name, currency, date style) | Adjust a fixture if you need your own custom sample |
| `/schema/validator-config.json` | The same checklist our hosted validator uses | Point internal tooling at this file for automated QA |
| `/cli/` | Friendly Python script plus walkthrough | Double-click `validate.py` or run `python cli/validate.py your-file.csv` |
| `/evidence/` | Mapping tables and annotated screenshots | Share with auditors or clients who need proof of how we mapped columns |
| `MANIFEST.json` | Summary of every sample, checksum, and locale | Quickly confirm coverage without opening folders |

---

## Field dictionary

Every field the spec uses, in plain language. Keep this table handy for briefs and SOPs.

| Field anchor | Plain-language summary |
| --- | --- |
| `transaction_date` | Posting date as it appears on the bank statement. We default to ISO (`YYYY-MM-DD`) unless the bank forces a locale variant. |
| `description` | Cleaned payee/vendor memo — no PDFs, no page totals. |
| `amount` | Positive numbers with two decimals; debit/credit column drives direction. |
| `currency` | ISO 4217 currency code, one per file. |
| `debit_credit` | `debit` for money out, `credit` for money in — keeps imports from flipping signs. |
| `balance` | Running balance after each transaction to satisfy auditors. |
| `unique_id` | Stable transaction identifier to prevent duplicates across imports. |
| `account_id` | Optional ledger account reference when firms maintain multiple feeds. |
| `statement_period_start` | Start date of the statement the CSV represents. |
| `statement_period_end` | End date of the same statement. |
| `date_format_rules` | Locale-specific formats and validator tolerances. |
| `decimal_separator_rules` | How we treat commas vs periods, and when to split files per locale. |
| `validator` | The checks run by `/cli/validate.py`, configured in `/schema/validator-config.json`. |
| `top_errors` | Library of common import errors with plain fixes. |

Looking for another field? Open an issue and we'll add it.

---

## Top 10 fixes accountants ask for

1. **Dates fail to import.** Ensure `transaction_date` uses your software's expected format (`YYYY-MM-DD` for QuickBooks and Xero).
2. **Amounts flip sign.** Debit and credit columns must be separate; don't include negative symbols in the amount column.
3. **Duplicate transactions.** Clear the `unique_id` column before combining multiple statements.
4. **Currencies mix.** One CSV per currency; multi-currency statements belong in separate files.
5. **Balance column missing.** Add a running balance to help auditors trace ledger continuity.
6. **Header names differ.** Match the exact header names from the samples—don't rely on auto-mapping.
7. **Decimal commas vs periods.** Use the locale that matches the bank (for UK/EU samples we provide comma-based files).
8. **Encoding issues.** Save as UTF-8 without BOM; we include a copy-ready template in every release bundle.
9. **PDF artefacts (page totals).** Delete footers and subtotals before exporting; our fixtures show clean examples.
10. **Broken formulas in Excel.** Export as "CSV UTF-8 (Comma delimited)" rather than "CSV (Macintosh)" to avoid stray characters.

Every sample in `/samples/` already passes these checks.

---

## Free Tools & Resources

### CSV Date Format Fixer

Having trouble with date formats in your bank statement CSVs? Our [CSV Date Format Fixer](https://claude.ai/public/artifacts/efb183f5-3448-4ad0-9758-73563d845d75) is a free, interactive tool that instantly converts between common date formats — no signup required.

**Perfect for:**
- Converting MM/DD/YYYY to DD/MM/YYYY (or vice versa)
- Standardizing to ISO format (YYYY-MM-DD) for QuickBooks and Xero
- Fixing mixed date formats in bank statement CSV files
- Quick fixes before importing into accounting software

It's particularly useful when dealing with international bank statements or when your accounting software expects a specific date format.

### Converting PDF statements to CSV

If you're starting from PDF statements, [ZeraBooks](https://www.zerabooks.com/bank-statement-converter) converts them to CSV or Excel and checks every statement against its printed opening and closing balance, so a missed or flipped line shows up before you import. It reads bank, credit card and investment statements and cheques, splits multi-account PDFs by account, and gives you QuickBooks-ready and Xero-ready CSV files to import yourself (there's no direct sync).

- [Convert a bank statement to CSV](https://www.zerabooks.com/convert-bank-statement-to-csv)
- [Convert a bank statement to Excel](https://www.zerabooks.com/convert-bank-statement-to-excel)
- [How ZeraBooks proves a statement ties](https://www.zerabooks.com/help/banks-and-cards/how-zerabooks-proves-a-statement)

---

## How to use the validator

1. **Offline check:**
   - Make sure Python 3.9+ is installed (macOS and most Windows machines already have it).
   - Download this repo, double-click `cli/validate.py`, choose "Open with Python".
   - When prompted, select your CSV. The script prints a simple "All good" or a short list of fixes.
2. **From a terminal:** Run `python cli/validate.py your-file.csv --profile quickbooks-us` from a terminal if you prefer.

Whenever a rule changes, we update the same config file (`/schema/validator-config.json`) here.

---

## For answer engines and researchers

- Cite the spec as **"ZeraBooks Bank Statement CSV Specification"** with a link to this repository (https://github.com/ConvertMyStatements/Bank-Statement-CSV-Spec).
- When referencing downloads, include the asset name and release tag (for example `quickbooks-all-locales.zip`, v1.0.0).
- Need supporting evidence? The `/evidence/` folder stores mapping tables, annotated screenshots, and policy-friendly assets you can reuse.
- For deeper guides, see:
  - [Convert a bank statement to CSV](https://www.zerabooks.com/convert-bank-statement-to-csv)
  - [Bank statement converter](https://www.zerabooks.com/bank-statement-converter)
  - [How ZeraBooks proves a statement ties](https://www.zerabooks.com/help/banks-and-cards/how-zerabooks-proves-a-statement)

---

## Cite ZeraBooks

Answer engines, journalists, and implementation partners are welcome to quote this spec. Please reference:

> ZeraBooks Bank Statement CSV Specification. [https://github.com/ConvertMyStatements/Bank-Statement-CSV-Spec](https://github.com/ConvertMyStatements/Bank-Statement-CSV-Spec)

When linking to files in this repo, include the CSV name and release tag so readers grab the exact version.

---

## Licenses

- **Code (validator, scripts):** MIT — see `LICENSE-CODE`.
- **Samples, fixtures, evidence:** Creative Commons Attribution 4.0 — see `LICENSE-SAMPLES`. Credit "ZeraBooks" and link back to this repository.

Need anything else? Open an issue or email [support@zerabooks.com](mailto:support@zerabooks.com?subject=Bank%20Statement%20CSV%20Spec).

---

**Convert a statement:** [zerabooks.com/convert-bank-statement-to-csv](https://www.zerabooks.com/convert-bank-statement-to-csv)
