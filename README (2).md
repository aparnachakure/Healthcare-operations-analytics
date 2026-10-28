# Power BI-ready package

This folder contains CSV exports that match the recommended star-schema handoff. The native `.pbix` report is intentionally not fabricated: it must be created in Power BI Desktop because the `.pbix` format is a proprietary desktop artifact.

## Import order

1. `DimDate.csv`
2. `DimPatient.csv`
3. `DimDepartment.csv`
4. `DimDoctor.csv`
5. `FactAdmissions.csv`
6. `FactTreatments.csv`
7. `FactBilling.csv`
8. `FactLabResults.csv`

## Relationships

- DimDate[Date] → FactAdmissions[admission_date]
- DimPatient[patient_id] → FactAdmissions[patient_id]
- DimDepartment[department_id] → FactAdmissions[department_id]
- DimDoctor[doctor_id] → FactAdmissions[doctor_id]
- FactAdmissions[admission_id] → FactTreatments[admission_id]
- FactAdmissions[admission_id] → FactBilling[admission_id]
- FactAdmissions[admission_id] → FactLabResults[admission_id]

Use single-direction filtering from dimensions to facts where possible.

## Suggested pages

1. Executive Overview — admissions, patients, readmissions, LOS, treatment cost, coverage.
2. Patient Analytics — demographics, city, insurance provider, diagnosis mix.
3. Hospital Operations — department volume, bed capacity, LOS, doctor workload.
4. Financial Analytics — gross charges, insurance coverage, out-of-pocket exposure.
5. Readmission Analytics — readmission rate by age, prior admissions, diagnosis and LOS band.

See `model-notes.md` and `measures.dax` for the semantic model and measures.
