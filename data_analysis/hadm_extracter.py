from csv_extract import csv_generator
import time
import json
LABEL = 0
HADM_ID = 2
TIME = 3
VALUE = 5

def get_hadm_dicts():
    current_hadm = 0
    current_date = time.struct_time((0,0,0,0,0,0,0,0,0))
    feature_dicts = {}
    p_csv = csv_generator("../dataset/sepsis-patients.csv")
    changed_hadm = False
    next(p_csv)
    for row in p_csv:
        row_time = time.strptime(row[TIME], '%Y-%m-%d %H:%M:%S')
        hadm = row[HADM_ID]
        label = row[LABEL]
        if not (int(row[HADM_ID]) == int(current_hadm)):
            feature_dicts[hadm] = []
            current_hadm = hadm
            changed_hadm = True
       
        if current_date.tm_hour != row_time.tm_hour or current_date.tm_mon != row_time.tm_mon:
            feature_dicts[hadm].append(get_init_dict())
            current_date = row_time
        elif changed_hadm:
            feature_dicts[hadm].append(get_init_dict())
            changed_hadm = False

        #if row[value] is not a string do the following
        try:
                amount = feature_dicts[hadm][-1][label][0] + 1
                value = float(row[VALUE])
                feature_dicts[hadm][-1][label][0] = amount
                feature_dicts[hadm][-1][label].append(value)
        #if row[VALUE] cannot be converted to a float
        except:
                amount = feature_dicts[hadm][-1][label][0] + 1
                value = row[VALUE]
                feature_dicts[hadm][-1][label][0] = amount
                feature_dicts[hadm][-1][label].append(value)
    for key in feature_dicts.keys():
        print("Amount of Hours for hadm",key,":",len(feature_dicts[key]))
    print(feature_dicts["175734"])
    return feature_dicts

def export_json(feature_dicts):
    with open("hadm_records.json", "w") as records:
        json.dump(feature_dicts, records, indent=4)

def get_init_dict():
    return {
        "Arterial BP [Systolic]":[0],
        "Eye Opening":[0],
        "FiO2 Set":[0],
        "Heart Rate":[0],
        "Manual BP [Systolic]":[0],
        "Motor Response":[0],
        "NBP [Systolic]":[0],
        "PAO2":[0],
        "SpO2":[0],
        "Temperature C":[0],
        "Temperature F":[0],
        "Verbal Response":[0],
        "Arterial PaO2":[0],
        "Platelets":[0],
        "FIO2":[0],
        "FIO2 [Meas]":[0],
        "Bilirubin":[0],
        "Creatinine":[0],
        "Arterial BP #2 [Systolic]":[0],
        "Skin Temperature":[0],
        "RV systolic pressure(PA Line)":[0],
        "PA systolic pressure(PA Line)":[0],
        "Bilirubin_ApacheIV":[0],
        "Direct Bilirubin":[0],
        "Total Bilirubin":[0],
        "Creatinine":[0],
        "GCS - Eye Opening":[0],
        "Heart Rate":[0],
        "Arterial Blood Pressure systolic":[0],
        "Non Invasive Blood Pressure systolic":[0],
        "Respiratory Rate":[0],
        "GCS - Verbal Response":[0],
        "GCS - Motor Response":[0],
        "Temperature Fahrenheit":[0],
        "Temperature Celsius":[0],
        "Inspired O2 Fraction":[0]
    }

if __name__ == '__main__':
    export_json(get_hadm_dicts())