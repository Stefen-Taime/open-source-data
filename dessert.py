import os
import json
import csv
import xml.etree.ElementTree as ET
import random
import uuid
from datetime import datetime

# Fonctions pour générer des valeurs aléatoires pour les desserts
def random_variety():
    return random.choice(["Doughnut", "Cake", "Pudding", "Cheesecake", "Pie", "Cookie"])

def random_topping():
    return random.choice(["Toffee Bits", "Walnuts", "Granola", "Mocha Drizzle", "Chocolate Chips", "Berry Compote", "Glaze"])

def random_flavor():
    return random.choice(["Peanut Butter", "Espresso", "Chocolate", "Butter Pecan", "Cookies 'n Cream", "Cherry"])


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

def create_dessert_xml(companies, file_path):
    root = ET.Element('Companies')
    for company in companies:
        company_elem = ET.SubElement(root, 'Computer')
        for key, val in company.items():
            child = ET.SubElement(company_elem, key)
            child.text = str(val)
    tree = ET.ElementTree(root)
    tree.write(file_path)


# Fonction pour écrire les données de dessert dans les fichiers correspondants
def write_dessert_data(desserts, dessert_folder, file_type, original_filename):
    output_folder = os.path.join(dessert_folder, file_type.strip('.'))
    os.makedirs(output_folder, exist_ok=True)
    output_path = os.path.join(output_folder, original_filename)

    if file_type == '.csv':
        with open(output_path, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=desserts[0].keys())
            writer.writeheader()
            for dessert in desserts:
                writer.writerow(dessert)
    elif file_type == '.json':
        with open(output_path, 'w') as file:
            json.dump(desserts, file, indent=4)
    elif file_type == '.xml':
        create_dessert_xml(desserts, output_path)

# Fonction pour traiter tous les fichiers dans un dossier pour les desserts
def process_dessert_files(directory, file_type, dessert_folder):
    for filename in os.listdir(directory):
        if filename.endswith(file_type):
            file_path = os.path.join(directory, filename)
            if file_type == '.csv':
                records = read_csv_file(file_path)
            elif file_type == '.json':
                records = read_json_file(file_path)
            elif file_type == '.xml':
                records = read_xml_file(file_path)

            desserts = []
            for record in records:
                dessert_data = {
                    "id": random.randint(1000, 9999),
                    "uid": str(uuid.uuid4()),
                    "variety": random_variety(),
                    "topping": random_topping(),
                    "flavor": random_flavor(),
                    "user_id": record['user_id'],  # Utiliser le user_id de l'enregistrement original
                    "dt_current_timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }
                desserts.append(dessert_data)

            write_dessert_data(desserts, dessert_folder, file_type, filename)

dessert_folder = '/home/stefen/data/dessert'
os.makedirs(dessert_folder, exist_ok=True)

csv_dir = '/home/stefen/data/bank/csv'
json_dir = '/home/stefen/data/bank/json'
xml_dir = '/home/stefen/data/bank/xml'

# Traitement des fichiers
process_dessert_files(csv_dir, '.csv', dessert_folder)
process_dessert_files(json_dir, '.json', dessert_folder)
process_dessert_files(xml_dir, '.xml', dessert_folder)