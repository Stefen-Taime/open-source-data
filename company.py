import os
import json
import csv
import xml.etree.ElementTree as ET
import random
import uuid
from datetime import datetime

# Fonctions pour générer des valeurs aléatoires pour les entreprises
def random_business_name():
    return random.choice(["Armstrong, Little and Cartwright", "Welch, Hagenes and Halvorson", "Smith Inc", "Doe Associates", "Johnson Corp"])

def random_suffix():
    return random.choice(["Inc", "LLC", "Group", "PLC", "Ltd"])

def random_industry():
    return random.choice(["Investment Management", "Dairy", "Technology", "Education", "Healthcare"])

def random_catch_phrase():
    return random.choice(["Seamless innovative synergy", "Revolutionary dynamic strategy", "Efficient scalable solution", "Proactive global mission"])

def random_buzzword():
    return random.choice(["Blockchain", "AI", "VR", "Synergy", "Big Data"])

def random_bs_statement():
    return random.choice(["enhance interactive platforms", "streamline cloud solutions", "optimize next-gen technologies", "revolutionize integrated markets"])

def random_ein():
    return f"{random.randint(10, 99)}-{random.randint(1000000, 9999999)}"

def random_duns_number():
    return f"{random.randint(10, 99)}-{random.randint(100, 999)}-{random.randint(1000, 9999)}"

def random_logo():
    return f"https://example.com/fake-logos/{random.randint(1, 10)}.png"

def random_phone_number():
    return f"+{random.randint(1, 999)} {random.randint(100, 999)}-{random.randint(1000, 9999)}-{random.randint(1000, 9999)}"

def random_address():
    return f"Suite {random.randint(1, 1000)} {random.randint(100, 99999)} Random Street, SomeCity, SomeCountry"

def random_latitude():
    return round(random.uniform(-90.0, 90.0), 6)

def random_longitude():
    return round(random.uniform(-180.0, 180.0), 6)


# Fonctions pour lire les fichiers CSV, JSON et XML
def read_csv_file(file_path):
    with open(file_path, mode='r', newline='') as file:
        reader = csv.DictReader(file)
        return list(reader)

def read_json_file(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def read_xml_file(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()
    records = []
    for record in root:
        record_data = {child.tag: child.text for child in record}
        records.append(record_data)
    return records

# Fonction pour créer un fichier XML pour les entreprises
def create_company_xml(companies, file_path):
    root = ET.Element('Companies')
    for company in companies:
        company_elem = ET.SubElement(root, 'Company')
        for key, val in company.items():
            child = ET.SubElement(company_elem, key)
            child.text = str(val)
    tree = ET.ElementTree(root)
    tree.write(file_path)

# Fonction pour écrire les données d'entreprise dans les fichiers correspondants
def write_company_data(companies, company_folder, file_type, original_filename):
    output_folder = os.path.join(company_folder, file_type.strip('.'))
    os.makedirs(output_folder, exist_ok=True)
    output_path = os.path.join(output_folder, original_filename)

    if file_type == '.csv':
        with open(output_path, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=companies[0].keys())
            writer.writeheader()
            for company in companies:
                writer.writerow(company)
    elif file_type == '.json':
        with open(output_path, 'w') as file:
            json.dump(companies, file, indent=4)
    elif file_type == '.xml':
        create_company_xml(companies, output_path)
        
# Fonction pour traiter tous les fichiers dans un dossier pour les entreprises
def process_company_files(directory, file_type, company_folder):
    for filename in os.listdir(directory):
        if filename.endswith(file_type):
            file_path = os.path.join(directory, filename)
            if file_type == '.csv':
                records = read_csv_file(file_path)
            elif file_type == '.json':
                records = read_json_file(file_path)
            elif file_type == '.xml':
                records = read_xml_file(file_path)

            companies = []
            for record in records:
                company_data = {
                    "id": random.randint(1000, 9999),
                    "uid": str(uuid.uuid4()),
                    "business_name": random_business_name(),
                    "suffix": random_suffix(),
                    "industry": random_industry(),
                    "catch_phrase": random_catch_phrase(),
                    "buzzword": random_buzzword(),
                    "bs_company_statement": random_bs_statement(),
                    "employee_identification_number": random_ein(),
                    "duns_number": random_duns_number(),
                    "logo": random_logo(),
                    "type": "Private",
                    "phone_number": random_phone_number(),
                    "full_address": random_address(),
                    "latitude": random_latitude(),
                    "longitude": random_longitude(),
                    "user_id": record['user_id'],  # Utiliser le user_id de l'enregistrement original
                    "dt_current_timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }
                companies.append(company_data)

            write_company_data(companies, company_folder, file_type, filename)

company_folder = '/home/stefen/data/company'
os.makedirs(company_folder, exist_ok=True)

csv_dir = '/home/stefen/data/bank/csv'
json_dir = '/home/stefen/data/bank/json'
xml_dir = '/home/stefen/data/bank/xml'

# Traitement des fichiers
process_company_files(csv_dir, '.csv', company_folder)
process_company_files(json_dir, '.json', company_folder)
process_company_files(xml_dir, '.xml', company_folder)