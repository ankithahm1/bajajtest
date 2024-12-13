import json
from collections import Counter
from datetime import datetime
import numpy as np

file_path = '/mnt/data/DataEngineeringQ2.json'
with open(file_path, 'r') as f:
    data = json.load(f)

patient_details = [entry['patientDetails'] for entry in data]
medicines = [med for entry in data for med in entry.get('consultationData', {}).get('medicines', [])]

def calculate_missing_percentage(field_name):
    total = len(patient_details)
    missing = sum(1 for patient in patient_details if not patient.get(field_name) or patient[field_name] in ["", None])
    return round((missing / total) * 100, 2)

first_name_missing = calculate_missing_percentage('firstName')
last_name_missing = calculate_missing_percentage('lastName')
dob_missing = calculate_missing_percentage('birthDate')

genders = [patient.get('gender') for patient in patient_details if patient.get('gender')]
mode_gender = Counter(genders).most_common(1)[0][0]
imputed_genders = [patient.get('gender', mode_gender) for patient in patient_details]
female_percentage = round((imputed_genders.count('F') / len(imputed_genders)) * 100, 2)

def calculate_age_group(birth_date):
    if not birth_date:
        return None
    age = datetime.now().year - datetime.fromisoformat(birth_date).year
    if age <= 12:
        return 'Child'
    elif 13 <= age <= 19:
        return 'Teen'
    elif 20 <= age <= 59:
        return 'Adult'
    else:
        return 'Senior'

age_groups = [calculate_age_group(patient.get('birthDate')) for patient in patient_details]
adult_count = age_groups.count('Adult')

average_medicines = round(sum(1 for med in medicines) / len(data), 2)

medicine_names = [med['medicineName'] for med in medicines]
third_most_common = Counter(medicine_names).most_common(3)[2][0]

active_medicines = sum(1 for med in medicines if med.get('isActive'))
inactive_medicines = sum(1 for med in medicines if not med.get('isActive'))
total_medicines = active_medicines + inactive_medicines
active_percentage = round((active_medicines / total_medicines) * 100, 2)
inactive_percentage = round((inactive_medicines / total_medicines) * 100, 2)

def is_valid_phone_number(phone_number):
    if not phone_number or not isinstance(phone_number, str):
        return False
    if phone_number.startswith('+91'):
        number = phone_number[3:]
    elif phone_number.startswith('91'):
        number = phone_number[2:]
    else:
        number = phone_number
    return number.isdigit() and 6000000000 <= int(number) <= 9999999999

phone_numbers = [entry.get('phoneNumber') for entry in data]
is_valid_mobile = [is_valid_phone_number(num) for num in phone_numbers]
valid_mobile_count = sum(is_valid_mobile)

medicines_count = [len(entry.get('consultationData', {}).get('medicines', [])) for entry in data]

patient_ages = []
for patient in patient_details:
    birth_date = patient.get('birthDate')
    if birth_date:
        age = datetime.now().year - datetime.fromisoformat(birth_date).year
        patient_ages.append(age)
    else:
        patient_ages.append(None)

filtered_data = [(m_count, age) for m_count, age in zip(medicines_count, patient_ages) if age is not None]
filtered_medicines_count, filtered_patient_ages = zip(*filtered_data)

pearson_correlation = round(np.corrcoef(filtered_medicines_count, filtered_patient_ages)[0, 1], 2)

(first_name_missing, last_name_missing, dob_missing, 
 female_percentage, adult_count, average_medicines, 
 third_most_common, active_percentage, inactive_percentage, 
 valid_mobile_count, pearson_correlation)
