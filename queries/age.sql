WITH first_admission_time AS (
SELECT 
    p.SUBJECT_ID, p.DOB, p.GENDER, 
    MIN (a.ADMITTIME) AS first_admittime
FROM PATIENTS p
INNER JOIN ADMISSIONS a
ON p.SUBJECT_ID = a.SUBJECT_ID
GROUP BY p.SUBJECT_ID, p.DOB, p.GENDER, a.HADM_ID
ORDER BY a.HADM_ID, p.SUBJECT_ID
),
age AS (
SELECT 
    SUBJECT_ID,
    cast(strftime('%Y.%m%d', first_admittime) - strftime('%Y.%m%d', DOB) as int) 
        AS first_admit_age, 
    CASE
        WHEN cast(strftime('%Y.%m%d', first_admittime) - strftime('%Y.%m%d', DOB) as int) > 89
            THEN '>89'
        WHEN cast(strftime('%Y.%m%d', first_admittime) - strftime('%Y.%m%d', DOB) as int) >= 15
            THEN 'adult'
        WHEN cast(strftime('%Y.%m%d', first_admittime) - strftime('%Y.%m%d', DOB) as int) <= 1
            THEN 'neonate'
        ELSE 'middle'
        END AS age_group
FROM first_admission_time
ORDER BY SUBJECT_ID
)
SELECT *
FROM age WHERE first_admit_age < 89;