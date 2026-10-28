-- Healthcare Operations Analytics: interview-ready SQL questions.
-- These queries answer the business questions defined in the project brief.

-- 1. Monthly admissions and readmission rate
SELECT
  DATE_TRUNC('month', a.admission_date)::date AS month,
  COUNT(*) AS admissions,
  ROUND(AVG(a.discharge_date - a.admission_date), 2) AS average_length_of_stay,
  ROUND(100.0 * AVG(CASE WHEN a.readmitted THEN 1 ELSE 0 END), 2) AS readmission_rate
FROM admissions a
GROUP BY 1
ORDER BY 1;

-- 2. Department performance
SELECT
  d.department_name,
  COUNT(*) AS admissions,
  ROUND(AVG(a.discharge_date - a.admission_date), 2) AS average_length_of_stay,
  ROUND(SUM(t.treatment_cost), 2) AS treatment_cost,
  ROUND(100.0 * AVG(CASE WHEN a.readmitted THEN 1 ELSE 0 END), 2) AS readmission_rate
FROM admissions a
JOIN departments d ON d.department_id = a.department_id
JOIN treatments t ON t.admission_id = a.admission_id
GROUP BY d.department_name
ORDER BY admissions DESC;

-- 3. Conditions associated with higher treatment cost
SELECT
  a.diagnosis,
  COUNT(*) AS admissions,
  ROUND(SUM(t.treatment_cost), 2) AS total_treatment_cost,
  ROUND(AVG(t.treatment_cost), 2) AS average_treatment_cost
FROM admissions a
JOIN treatments t ON t.admission_id = a.admission_id
GROUP BY a.diagnosis
ORDER BY average_treatment_cost DESC;

-- 4. Doctors with the highest patient volume, using a window rank
WITH doctor_volume AS (
  SELECT
    d.doctor_name,
    dep.department_name,
    COUNT(DISTINCT a.patient_id) AS unique_patients,
    COUNT(*) AS admissions
  FROM admissions a
  JOIN doctors d ON d.doctor_id = a.doctor_id
  JOIN departments dep ON dep.department_id = a.department_id
  GROUP BY d.doctor_name, dep.department_name
)
SELECT
  *,
  DENSE_RANK() OVER (ORDER BY admissions DESC) AS volume_rank
FROM doctor_volume
ORDER BY volume_rank, doctor_name;

-- 5. Patient-level out-of-pocket exposure using a CTE
WITH patient_costs AS (
  SELECT
    p.patient_id,
    p.insurance_provider,
    COUNT(a.admission_id) AS admissions,
    SUM(b.out_of_pocket_cost) AS out_of_pocket_cost
  FROM patients p
  JOIN admissions a ON a.patient_id = p.patient_id
  JOIN billing b ON b.admission_id = a.admission_id
  GROUP BY p.patient_id, p.insurance_provider
)
SELECT *
FROM patient_costs
ORDER BY out_of_pocket_cost DESC
LIMIT 20;

-- 6. Readmission segments for the ML feature review
SELECT
  CASE
    WHEN EXTRACT(YEAR FROM AGE(a.admission_date, p.date_of_birth)) < 35 THEN 'Under 35'
    WHEN EXTRACT(YEAR FROM AGE(a.admission_date, p.date_of_birth)) < 55 THEN '35-54'
    WHEN EXTRACT(YEAR FROM AGE(a.admission_date, p.date_of_birth)) < 75 THEN '55-74'
    ELSE '75+'
  END AS age_group,
  COUNT(*) AS admissions,
  SUM(CASE WHEN a.readmitted THEN 1 ELSE 0 END) AS readmissions,
  ROUND(100.0 * AVG(CASE WHEN a.readmitted THEN 1 ELSE 0 END), 2) AS readmission_rate
FROM admissions a
JOIN patients p ON p.patient_id = a.patient_id
GROUP BY 1
ORDER BY 1;