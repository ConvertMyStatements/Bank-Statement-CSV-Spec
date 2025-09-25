# Sample CSV Library

These sample files show exactly how successful imports should look in QuickBooks, Xero, Sage, Zoho, Wave, and FreshBooks across the United States, Canada, United Kingdom, Australia, and New Zealand.

## Folder map

```
samples/
  quickbooks/
  xero/
  sage/
  zoho/
  wave/
  freshbooks/
  edge-cases/
```

Each file name follows `{bank}__{software}__{locale-or-note}.csv`. Example: `chase__quickbooks__us-standard.csv`.

Edge cases cover the most common “uh-oh” scenarios (duplicate rows, decimal commas, merged statements) so you can test your own guardrails.

> Every bundle links back to [ConvertMyStatements](https://www.convertmystatements.com/?utm_source=github&utm_medium=repo&utm_campaign=bank_statement_csv_spec). If you need a custom format, upload your PDF there and we’ll handle it for you.
