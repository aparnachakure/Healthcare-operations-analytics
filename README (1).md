# Excel inspection checklist

Excel is used for initial data understanding, not the primary cleaning engine.

## Workbook tabs

1. `Raw_Admissions` — inspect date fields, duplicate admission IDs, invalid ages, and category spelling.
2. `Raw_Patients` — check missing demographics, insurance labels, and patient ID uniqueness.
3. `Quality_Checks` — pivot counts for blanks, duplicate IDs, negative stays, and unusual treatment costs.
4. `Initial_Pivots` — admissions by department/month, condition mix, and readmission rate.

## Suggested formulas

- Missing values: `=COUNTBLANK(A:A)`
- Duplicate IDs: `=COUNTIF($A:$A,A2)>1`
- Length of stay: `=Discharge_Date-Admission_Date`
- Out-of-pocket check: `=Gross_Charge-Insurance_Coverage`

The workbook should preserve a raw copy, document each quality issue, and link to the
cleaned output produced by `analytics/python/clean_healthcare_data.py`.