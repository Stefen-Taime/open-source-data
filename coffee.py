import os
import json
import csv
import xml.etree.ElementTree as ET
import uuid
import random
from datetime import datetime

# Fonctions pour générer des valeurs aléatoires pour le café
def random_blend_name():
    return random.choice(["American Volcano", "Major Solstice", "The Blend", "Strong Forrester", "Melty America"])

def random_origin():
    return random.choice(["Sul Minas, Brazil", "Kigeyo Washing Station, Rwanda", "Mount Elgon, Uganda", "Mattari, Yemen", "Granada, Nicaragua"])

def random_variety():
    return random.choice(["S288", "Pink Bourbon", "Liberica", "Red Bourbon", "Java"])

def random_notes():
    return random.choice(["delicate, coating, sundried tomato, grapefruit, coriander",
                          "astringent, tea-like, toast, cacao nibs, barley",
                          "bright, velvety, liquorice, red currant, bakers chocolate",
                          "astringent, tea-like, green grape, wheat, rubber",
                          "mild, coating, cinnamon, dill, dates"])

def random_intensifier():
    return random.choice(["soft", "juicy", "deep", "astringent", "pointed"])

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

# Fonction pour créer un fichier XML pour le café
def create_coffee_xml(coffees, file_path):
    root = ET.Element('Coffees')
    for coffee in coffees:
        coffee_elem = ET.SubElement(root, 'Coffee')
        for key, val in coffee.items():
            child = ET.SubElement(coffee_elem, key)
            child.text = str(val)
    tree = ET.ElementTree(root)
    tree.write(file_path)

# Fonction pour écrire les données de café dans les fichiers correspondants
def write_coffee_data(coffees, coffee_folder, file_type, original_filename):
    output_folder = os.path.join(coffee_folder, file_type.strip('.'))
    os.makedirs(output_folder, exist_ok=True)
    output_path = os.path.join(output_folder, original_filename)

    if file_type == '.csv':
        with open(output_path, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=coffees[0].keys())
            writer.writeheader()
            for coffee in coffees:
                writer.writerow(coffee)
    elif file_type == '.json':
        with open(output_path, 'w') as file:
            json.dump(coffees, file, indent=4)
    elif file_type == '.xml':
        create_coffee_xml(coffees, output_path)

current_date = datetime.now().strftime('%Y%m%d')

# Fonction pour traiter tous les fichiers dans un dossier pour le café
def process_coffee_files(directory, file_type, coffee_folder):
    for filename in os.listdir(directory):
        if filename.endswith(file_type):
            file_path = os.path.join(directory, filename)
            if file_type == '.csv':
                records = read_csv_file(file_path)
            elif file_type == '.json':
                records = read_json_file(file_path)
            elif file_type == '.xml':
                records = read_xml_file(file_path)

            coffees = []
            for record in records:
                coffee_data = {
                    "blend_name": random_blend_name(),
                    "origin": random_origin(),
                    "variety": random_variety(),
                    "notes": random_notes(),
                    "intensifier": random_intensifier(),
                    "user_id": record['user_id'],  # Utilisez le user_id de l'enregistrement original
                    "dt_current_timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }
                coffees.append(coffee_data)

            # Écrivez toutes les données de café après la boucle pour éviter de réécrire à chaque itération
            write_coffee_data(coffees, coffee_folder, file_type, filename)


csv_dir = '/home/stefen/data/bank/csv'
json_dir = '/home/stefen/data/bank/json'
xml_dir = '/home/stefen/data/bank/xml'

coffee_folder = '/home/stefen/data/coffee'
os.makedirs(coffee_folder, exist_ok=True)

process_coffee_files(csv_dir, '.csv', coffee_folder)
process_coffee_files(json_dir, '.json', coffee_folder)
process_coffee_files(xml_dir, '.xml', coffee_folder)



