


With complete_record as (
    SELECT i.label, p.subject_id, c.charttime,c.value, c.valuenum,
    c.valueuom 
    FROM patients AS p 
    INNER JOIN chartevents AS c 
    ON p.subject_id = c.subject_id 
    LEFT JOIN d_items AS i ON c.itemid = i.itemid WHERE 
    i.itemid = 226850 -- RV systolic pressure(PA Line)
    OR i.itemid = 226852 -- PA systolic pressure(PA Line)
    OR i.itemid = 220045 -- HEART RATE
    OR i.itemid = 223762 -- TEMPERATURE CELSIUS
    OR i.itemid = 646 -- SPO2
    OR i.itemid = 220210 -- RESPIRATORY RATE
    OR i.itemid = 224027 -- SKIN TEMPERATURE
    OR i.itemid = 723 -- GCSVerbal Carevue
    OR i.itemid = 454 -- GCSMotor Carevue
    OR i.itemid = 184 -- GSCEyes 
    OR i.itemid = 223900 -- GCS Verbal Metavision
    OR i.itemid = 220210 -- Respiratory Rate 
    OR i.itemid = 224027 -- SKIN TEMPERATURE
    OR i.itemid = 223901 -- GCS MOTOR Metavision
    OR i.itemid = 220739 -- Eye Opening
    OR i.itemid = 51 -- Arterial BP [Systolic]
    OR i.itemid = 442 -- Manual BP [Systolic]
    OR i.itemid = 455 -- NBP [Systolic]
    OR i.itemid = 6701 -- Arterial BP #2 [Systolic]
    OR i.itemid =  220179 -- Non Invasive Blood Pressure systolic
    OR i.itemid = 220050 -- Arterial Blood Pressure systolic
    OR i.itemid = 211 -- Heart Rate Care Vue 
    OR i.itemid = 678 -- Temperature F 
    OR i.itemid = 223761 -- Temperature Fahrenheit Metavision
    OR i.itemid = 676 -- Temperature C 
    OR i.itemid = 223835 -- Inspired O2 Fraction (FiO2)
    OR i.itemid = 3420 -- FiO2
    OR i.itemid = 3422 -- FiO2 [Meas]
    OR i.itemid = 190 -- FiO2 set
    OR i.itemid = 779 -- Arterial PaO2 carevue
    OR i.itemid = 490 -- PAO2 carevue
    OR i.itemid = 4948 -- Bilirubin
    OR i.itemid =  226998 -- Bilirubin_ApacheIV metavision
    OR i.itemid = 225651 -- Direct Bilirubin  metavision
    OR i.itemid =  225690 -- Total Bilirubin metavision
    OR i.itemid = 1525 -- Creatinine chartevents
    OR i.itemid = 220615 -- Creatinine metavision
    OR i.itemid = 828 -- Platelets carevue
    
    ORDER BY p.subject_id, c.charttime 
)


Select * from complete_record where subject_id in (
    select p.subject_id 
    from patients as p 
    inner join 
    diagnoses_icd as di 
    on p.subject_id = di.subject_id
    where di.icd9_code = '99591' OR di.icd9_code = '99592'
    group by p.subject_id
);


