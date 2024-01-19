import os
import json
import csv
import xml.etree.ElementTree as ET
import random
import uuid
from datetime import datetime

# Fonctions pour générer des valeurs aléatoires pour les ordinateurs
def random_platform():
    return random.choice(["Linux", "macOS", "Windows"])

def random_type():
    return random.choice(["workstation", "server"])

def random_os():
    return random.choice(["CentOS 8", "Windows 10", "RHEL 7.7", "High Sierra (10.13)", "Ubuntu Desktop 18.04"])

def random_stack():
    return ", ".join(random.sample(["Windows", "macOS", "Linux", "Ubuntu", "RHEL"], 2))

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

def create_computer_xml(companies, file_path):
    root = ET.Element('Companies')
    for company in companies:
        company_elem = ET.SubElement(root, 'Computer')
        for key, val in company.items():
            child = ET.SubElement(company_elem, key)
            child.text = str(val)
    tree = ET.ElementTree(root)
    tree.write(file_path)

# Fonction pour écrire les données d'ordinateur dans les fichiers correspondants
def write_computer_data(computers, computer_folder, file_type, original_filename):
    output_folder = os.path.join(computer_folder, file_type.strip('.'))
    os.makedirs(output_folder, exist_ok=True)
    output_path = os.path.join(output_folder, original_filename)

    if file_type == '.csv':
        with open(output_path, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=computers[0].keys())
            writer.writeheader()
            for computer in computers:
                writer.writerow(computer)
    elif file_type == '.json':
        with open(output_path, 'w') as file:
            json.dump(computers, file, indent=4)
    elif file_type == '.xml':
        create_computer_xml(computers, output_path)

# Fonction pour traiter tous les fichiers dans un dossier pour les ordinateurs
def process_computer_files(directory, file_type, computer_folder):
    for filename in os.listdir(directory):
        if filename.endswith(file_type):
            file_path = os.path.join(directory, filename)
            if file_type == '.csv':
                records = read_csv_file(file_path)
            elif file_type == '.json':
                records = read_json_file(file_path)
            elif file_type == '.xml':
                records = read_xml_file(file_path)

            computers = []
            for record in records:
                computer_data = {
                    "id": random.randint(1000, 9999),
                    "uid": str(uuid.uuid4()),
                    "platform": random_platform(),
                    "type": random_type(),
                    "os": random_os(),
                    "stack": random_stack(),
                    "user_id": record['user_id'],  # Utiliser le user_id de l'enregistrement original
                    "dt_current_timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }
                computers.append(computer_data)

            write_computer_data(computers, computer_folder, file_type, filename)

computer_folder = '/home/stefen/data/computer'
os.makedirs(computer_folder, exist_ok=True)

csv_dir = '/home/stefen/data/bank/csv'
json_dir = '/home/stefen/data/bank/json'
xml_dir = '/home/stefen/data/bank/xml'

# Traitement des fichiers
process_computer_files(csv_dir, '.csv', computer_folder)
process_computer_files(json_dir, '.json', computer_folder)
process_computer_files(xml_dir, '.xml', computer_folder)
