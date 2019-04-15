select p.subject_id, di.icd9_code 
from patients as p 
inner join 
diagnoses_icd as di 
on p.subject_id = di.subject_id
where di.icd9_code = '99591' OR di.icd9_code = '99592' order by p.subject_id;

--- 99591 -> Sepsis 99592 -> Severe Sepsis --- 