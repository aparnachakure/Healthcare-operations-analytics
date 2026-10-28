# Power BI model handoff

## Recommended model

Use a star-shaped reporting model rather than loading one wide admissions table.

- `FactAdmissions` — one row per admission, with admission dates, department,
  doctor, diagnosis, length of stay, previous admissions, and readmission flag.
- `FactBilling` — one row per admission, with gross charge, insurance coverage,
  and out-of-pocket cost.
- `FactTreatments` — one row per admission, with treatment type and cost.
- `DimPatient` — patient demographics and insurance provider.
- `DimDepartment` — department name, type, and bed capacity.
- `DimDoctor` — doctor name, specialty, and department.
- `DimDate` — a dedicated calendar table related to `FactAdmissions[AdmissionDate]`.

Keep relationships single-directional from dimensions to facts. Mark `DimDate`
as the date table and use measures for aggregations instead of duplicating
calculated columns in each report page.

## Suggested report pages

1. Executive Overview
2. Patient Analytics
3. Hospital Operations
4. Financial Analytics
5. Readmission Analytics

## Refresh note

The dashboard and SQL layer currently use the same synthetic PostgreSQL source.
For Power BI, import the cleaned relational tables or connect to the SQL
database and preserve the measure definitions below.