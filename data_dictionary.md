# Healthcare analytics data dictionary

| Table | Field | Meaning | Type |
| --- | --- | --- | --- |
| departments | department_id | Unique department identifier | Text |
| departments | department_name | Reporting name for the hospital department | Text |
| departments | department_type | Acute, specialty, or women and children grouping | Text |
| departments | bed_capacity | Planned staffed beds | Integer |
| doctors | doctor_id | Unique physician identifier | Text |
| doctors | doctor_name | Display name for operational reporting | Text |
| doctors | specialty | Primary medical specialty | Text |
| patients | patient_id | Unique patient identifier | Text |
| patients | date_of_birth | Date used to derive age at admission | Date |
| patients | gender | Patient gender category | Text |
| patients | city | Patient home city | Text |
| patients | insurance_provider | Coverage provider or self-pay flag | Text |
| admissions | admission_id | Unique hospital encounter identifier | Text |
| admissions | patient_id | Patient linked to the encounter | Text / FK |
| admissions | doctor_id | Attending doctor | Text / FK |
| admissions | department_id | Department responsible for the encounter | Text / FK |
| admissions | admission_date | Date the encounter started | Date |
| admissions | discharge_date | Date the encounter ended | Date |
| admissions | admission_type | Emergency, urgent, or elective | Text |
| admissions | diagnosis | Primary condition used for reporting | Text |
| admissions | previous_admissions | Prior admissions known at encounter time | Integer |
| admissions | readmitted | Whether the patient returned within the project definition | Boolean |
| treatments | treatment_cost | Cost assigned to the encounter treatment | Decimal |
| billing | gross_charge | Total gross charge | Decimal |
| billing | insurance_coverage | Amount covered by insurance | Decimal |
| billing | out_of_pocket_cost | Gross charge not covered by insurance | Decimal |
| lab_results | result_flag | Simplified normal, high, or low quality flag | Text |

## Derived analytical fields

- `age` and `age_group`
- `length_of_stay` and `length_of_stay_band`
- `out_of_pocket_cost`
- `readmission_flag`
- `previous_admission_band`

All monetary values are synthetic portfolio-demo values displayed in Indian rupees (₹). They are not real healthcare prices, reimbursement rates, or financial benchmarks.