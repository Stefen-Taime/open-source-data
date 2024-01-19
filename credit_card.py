import os
import json
import csv
import xml.etree.ElementTree as ET
import random
import uuid
from datetime import datetime

# Fonctions pour générer des valeurs aléatoires pour les cartes de crédit
def random_credit_card_number():
    return f"{random.randint(1000, 9999)}-{random.randint(1000, 9999)}-{random.randint(1000, 9999)}-{random.randint(1000, 9999)}"

def random_credit_card_expiry_date():
    year = random.randint(2021, 2030)
    month = random.randint(1, 12)
    return f"{year}-{month:02d}-01"

def random_credit_card_type():
    return random.choice(["visa", "mastercard", "discover", "diners_club", "laser"])



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

def create_credit_card_xml(companies, file_path):
    root = ET.Element('Companies')
    for company in companies:
        company_elem = ET.SubElement(root, 'Computer')
        for key, val in company.items():
            child = ET.SubElement(company_elem, key)
            child.text = str(val)
    tree = ET.ElementTree(root)
    tree.write(file_path)

    # Fonction pour écrire les données de carte de crédit dans les fichiers correspondants
def write_credit_card_data(credit_cards, credit_card_folder, file_type, original_filename):
    output_folder = os.path.join(credit_card_folder, file_type.strip('.'))
    os.makedirs(output_folder, exist_ok=True)
    output_path = os.path.join(output_folder, original_filename)

    if file_type == '.csv':
        with open(output_path, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=credit_cards[0].keys())
            writer.writeheader()
            for credit_card in credit_cards:
                writer.writerow(credit_card)
    elif file_type == '.json':
        with open(output_path, 'w') as file:
            json.dump(credit_cards, file, indent=4)
    elif file_type == '.xml':
        create_credit_card_xml(credit_cards, output_path)

# Fonction pour traiter tous les fichiers dans un dossier pour les cartes de crédit
def process_credit_card_files(directory, file_type, credit_card_folder):
    for filename in os.listdir(directory):
        if filename.endswith(file_type):
            file_path = os.path.join(directory, filename)
            if file_type == '.csv':
                records = read_csv_file(file_path)
            elif file_type == '.json':
                records = read_json_file(file_path)
            elif file_type == '.xml':
                records = read_xml_file(file_path)

            credit_cards = []
            for record in records:
                credit_card_data = {
                    "id": random.randint(1000, 9999),
                    "uid": str(uuid.uuid4()),
                    "credit_card_number": random_credit_card_number(),
                    "credit_card_expiry_date": random_credit_card_expiry_date(),
                    "credit_card_type": random_credit_card_type(),
                    "user_id": record['user_id'],  # Utiliser le user_id de l'enregistrement original
                    "dt_current_timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }
                credit_cards.append(credit_card_data)

            write_credit_card_data(credit_cards, credit_card_folder, file_type, filename)

credit_card_folder = '/home/stefen/data/credit_card'
os.makedirs(credit_card_folder, exist_ok=True)

csv_dir = '/home/stefen/data/bank/csv'
json_dir = '/home/stefen/data/bank/json'
xml_dir = '/home/stefen/data/bank/xml'

# Traitement des fichiers
process_credit_card_files(csv_dir, '.csv', credit_card_folder)
process_credit_card_files(json_dir, '.json', credit_card_folder)
process_credit_card_files(xml_dir, '.xml', credit_card_folder)