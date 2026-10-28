# Power BI build guide

This project is already prepared for a native Power BI report. The steps below turn the supplied CSV package into the final `.pbix` artifact in Power BI Desktop.

## 1. Load the tables

Open Power BI Desktop → **Get Data → Text/CSV** and import every CSV in `analytics/powerbi/data/`. Rename tables if needed to match the names below.

## 2. Create relationships

Use **Model view** and create these relationships:

| From | To | Cardinality |
|---|---|---|
| DimDate[Date] | FactAdmissions[admission_date] | 1 → many |
| DimPatient[patient_id] | FactAdmissions[patient_id] | 1 → many |
| DimDepartment[department_id] | FactAdmissions[department_id] | 1 → many |
| DimDoctor[doctor_id] | FactAdmissions[doctor_id] | 1 → many |
| FactAdmissions[admission_id] | FactTreatments[admission_id] | 1 → 1 |
| FactAdmissions[admission_id] | FactBilling[admission_id] | 1 → 1 |
| FactAdmissions[admission_id] | FactLabResults[admission_id] | 1 → 1 |

Set cross-filter direction to **Single** wherever possible. Mark `DimDate` as the date table.

## 3. Add measures

Copy the measures from `measures.dax` into the model.

## 4. Build five pages

### Executive Overview
KPI cards: Total Patients, Total Admissions, Average Length of Stay, Readmissions, Readmission Rate, Total Treatment Cost, Coverage Rate. Add monthly admissions line chart and department volume bar chart.

### Patient Analytics
Use age group, gender, city, insurance provider, diagnosis and admission type. Add slicers for Date, Department, Diagnosis and Admission Type.

### Hospital Operations
Show admissions by department, average LOS, admissions per bed, doctor volume and treatment outcomes.

### Financial Analytics
Show gross charges, insurance coverage, out-of-pocket cost, coverage rate, treatment cost by department and diagnosis.

### Readmission Analytics
Show readmission rate by age group, previous-admission band, diagnosis and LOS band. Clearly label the page as **synthetic analytical demonstration — not a clinical risk tool**.

## 5. Formatting

- Use Indian number formatting for currency (₹).
- Keep titles short and business-oriented.
- Prefer accessible contrast and avoid unnecessary chart decoration.
- Add a footer: `Synthetic data • Portfolio demonstration • Not clinical or financial advice`.

## 6. Save

Save the completed report as `Healthcare_Operations_Analytics.pbix` in this folder. The repository intentionally does not include a generated placeholder `.pbix`; the real file should come from Power BI Desktop.
