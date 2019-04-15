import csv
import os
SEPSIS_DIR = os.path.abspath(__file__).replace("csv_extract.py", "sepsis-patients.csv")

def csv_sepsis_generator(sepsis_dir=SEPSIS_DIR):
    with open(sepsis_dir, 'r') as sepsis_file:
        csv_reader = csv.reader(sepsis_file)
        for row in csv_reader:
            yield row

if __name__ == "__main__":
    for row in csv_sepsis_generator():
        print(row)