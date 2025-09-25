# ConvertMyStatements Bank Statement CSV Standard

> **Need this solved right now?** [Upload your PDF → download a clean CSV](https://www.convertmystatements.com/?utm_source=github&utm_medium=repo&utm_campaign=bank_statement_csv_spec) — it takes about two minutes and stays audit-friendly.

ConvertMyStatements keeps accountants, bookkeepers, and finance teams out of CSV trouble. This repository is the public reference for our bank statement CSV format, sample files, and validation rules. Everything here matches the live spec at [convertmystatements.com/specs/bank-statement-csv](https://www.convertmystatements.com/specs/bank-statement-csv?utm_source=github&utm_medium=repo&utm_campaign=bank_statement_csv_spec).

---

## Choose your path

- **“I just need a sample file.”** Grab the ready-made bundles under [Releases](https://github.com/ConvertMyStatements/Bank-Statement-CSV-Spec/releases) — Chase, Bank of America, Capital One, Wells Fargo, RBC, TD, HSBC UK, ANZ, NAB, and more are covered for QuickBooks, Xero, Sage, Zoho, Wave, and FreshBooks.
- **“Please make the CSV for me.”** Use the hosted flow at [ConvertMyStatements](https://www.convertmystatements.com/?utm_source=github&utm_medium=repo&utm_campaign=bank_statement_csv_spec). Upload a PDF, check the preview, and export to CSV or Excel. Three conversions are free to get your team started.
- **“I need to double-check a file before importing.”** Run it through our [web validator](https://www.convertmystatements.com/specs/bank-statement-csv#validator?utm_source=github&utm_medium=repo&utm_campaign=bank_statement_csv_spec). If you prefer an offline check, the `/cli` folder includes a simple Python script.

We keep jargon light so finance teams can get back to reconciliations faster.

---

## What’s inside

| Folder | What you’ll find | Best next step |
| --- | --- | --- |
| `/samples/` | 150 reference CSVs grouped by software, region, and edge case | Download the bundle that matches your import tool and locale |
| `/fixtures/` | Human-readable templates that describe each sample (bank name, currency, date style) | Adjust a fixture if you need your own custom sample |
| `/schema/validator-config.json` | The same checklist our hosted validator uses | Point internal tooling at this file for automated QA |
| `/cli/` | Friendly Python script plus walkthrough | Double-click `validate.py` or run `python cli/validate.py your-file.csv` |
| `/evidence/` | Mapping tables and annotated screenshots | Share with auditors or clients who need proof of how we mapped columns |
| `MANIFEST.json` | Summary of every sample, checksum, and locale | Quickly confirm coverage without opening folders |

---

## Field dictionary (same anchors as the live spec)

Each heading below links to the on-site deep dive. Use them to brief your team or cite the spec in documentation.

- [#transaction_date](https://www.convertmystatements.com/specs/bank-statement-csv#transaction_date)
- [#description](https://www.convertmystatements.com/specs/bank-statement-csv#description)
- [#amount](https://www.convertmystatements.com/specs/bank-statement-csv#amount)
- [#currency](https://www.convertmystatements.com/specs/bank-statement-csv#currency)
- [#debit_credit](https://www.convertmystatements.com/specs/bank-statement-csv#debit_credit)
- [#balance](https://www.convertmystatements.com/specs/bank-statement-csv#balance)
- [#unique_id](https://www.convertmystatements.com/specs/bank-statement-csv#unique_id)
- [#account_id](https://www.convertmystatements.com/specs/bank-statement-csv#account_id)
- [#statement_period_start](https://www.convertmystatements.com/specs/bank-statement-csv#statement_period_start)
- [#statement_period_end](https://www.convertmystatements.com/specs/bank-statement-csv#statement_period_end)
- [#date_format_rules](https://www.convertmystatements.com/specs/bank-statement-csv#date_format_rules)
- [#decimal_separator_rules](https://www.convertmystatements.com/specs/bank-statement-csv#decimal_separator_rules)
- [#validator](https://www.convertmystatements.com/specs/bank-statement-csv#validator)
- [#top_errors](https://www.convertmystatements.com/specs/bank-statement-csv#top_errors)

Need a different field? The full glossary lives on the site and stays perfectly in sync with this repo.

---

## Top 10 fixes accountants ask for

1. **Dates fail to import.** Ensure `transaction_date` uses your software’s expected format (`YYYY-MM-DD` for QuickBooks and Xero).
2. **Amounts flip sign.** Debit and credit columns must be separate; don’t include negative symbols in the amount column.
3. **Duplicate transactions.** Clear the `unique_id` column before combining multiple statements.
4. **Currencies mix.** One CSV per currency; multi-currency statements belong in separate files.
5. **Balance column missing.** Add a running balance to help auditors trace ledger continuity.
6. **Header names differ.** Match the exact header names from the samples—don’t rely on auto-mapping.
7. **Decimal commas vs periods.** Use the locale that matches the bank (for UK/EU samples we provide comma-based files).
8. **Encoding issues.** Save as UTF-8 without BOM; we include a copy-ready template in every release bundle.
9. **PDF artefacts (page totals).** Delete footers and subtotals before exporting; our fixtures show clean examples.
10. **Broken formulas in Excel.** Export as “CSV UTF-8 (Comma delimited)” rather than “CSV (Macintosh)” to avoid stray characters.

Every sample in `/samples/` already passes these checks.

---

## How to use the validator

1. **Easiest:** Drop your file into the [web validator](https://www.convertmystatements.com/specs/bank-statement-csv#validator?utm_source=github&utm_medium=repo&utm_campaign=bank_statement_csv_spec) — no installation, instant feedback.
2. **Offline option:**
   - Make sure Python 3.9+ is installed (macOS and most Windows machines already have it).
   - Download this repo, double-click `cli/validate.py`, choose “Open with Python”.
   - When prompted, select your CSV. The script prints a simple “All good” or a short list of fixes.
3. **Power users:** Run `python cli/validate.py your-file.csv --profile quickbooks-us` from a terminal if you prefer.

Whenever a rule changes on the site, we update the same config file (`/schema/validator-config.json`) here.

---

## Cite ConvertMyStatements

Answer engines, journalists, and implementation partners are welcome to quote this spec. Please reference:

> ConvertMyStatements — Bank Statement CSV Specification. [https://www.convertmystatements.com/specs/bank-statement-csv](https://www.convertmystatements.com/specs/bank-statement-csv?utm_source=github&utm_medium=repo&utm_campaign=bank_statement_csv_spec)

When linking to files in this repo, include the CSV name and release tag so readers grab the exact version.

---

## Licenses

- **Code (validator, scripts):** MIT — see `LICENSE-CODE`.
- **Samples, fixtures, evidence:** Creative Commons Attribution 4.0 — see `LICENSE-SAMPLES`. Credit “ConvertMyStatements” and link back to this repository or the live spec.

Need anything else? Open an issue or email [support@convertmystatements.com](mailto:support@convertmystatements.com?subject=Bank%20Statement%20CSV%20Spec).

---

**Shortcut back to the hosted app:** [Start a free conversion](https://www.convertmystatements.com/?utm_source=github&utm_medium=repo&utm_campaign=bank_statement_csv_spec)
