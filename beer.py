import os
import json
import csv
import xml.etree.ElementTree as ET
import uuid
import random


# Fonction pour lire les fichiers CSV
def read_csv_file(file_path):
    with open(file_path, mode='r', newline='') as file:
        reader = csv.DictReader(file)
        return list(reader)

# Fonction pour lire les fichiers JSON
def read_json_file(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

# Fonction pour lire les fichiers XML
def read_xml_file(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()
    records = []
    for record in root:
        record_data = {child.tag: child.text for child in record}
        records.append(record_data)
    return records

# Fonction pour traiter tous les fichiers dans un dossier
def process_files(directory, file_type):
    for filename in os.listdir(directory):
        if filename.endswith(file_type):
            file_path = os.path.join(directory, filename)
            if file_type == '.csv':
                records = read_csv_file(file_path)
            elif file_type == '.json':
                records = read_json_file(file_path)
            elif file_type == '.xml':
                records = read_xml_file(file_path)

            # Utiliser le user_id de chaque enregistrement des fichiers bank
            beers = []
            for record in records:
                beer_data = {
                    "brand": random_brand(),
                    "name": random_name(),
                    "style": random_style(),
                    "hop": random_hop(),
                    "yeast": random_yeast(),
                    "malts": random_malts(),
                    "ibu": random_ibu(),
                    "alcohol": random_alcohol(),
                    "blg": random_blg(),
                    "user_id": record['user_id']  
                }
                beers.append(beer_data)
            
            # Écrire dans les fichiers de beer
            write_beer_data(beers, beer_folder, file_type, filename)




# Fonction pour créer un fichier XML
def create_beer_xml(beers, file_path):
    root = ET.Element('Beers')
    for beer in beers:
        beer_elem = ET.SubElement(root, 'Beer')
        for key, val in beer.items():
            child = ET.SubElement(beer_elem, key)
            child.text = str(val)
    tree = ET.ElementTree(root)
    tree.write(file_path)

# Écrire les données de bière dans les fichiers correspondants
def write_beer_data(beers, beer_folder, file_type, original_filename):
    # Déterminer le chemin du fichier de sortie
    output_folder = os.path.join(beer_folder, file_type.strip('.'))
    os.makedirs(output_folder, exist_ok=True)
    output_path = os.path.join(output_folder, original_filename)

    if file_type == '.csv':
        # Écrire en CSV
        with open(output_path, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=beers[0].keys())
            writer.writeheader()
            for beer in beers:
                writer.writerow(beer)
    elif file_type == '.json':
        # Écrire en JSON
        with open(output_path, 'w') as file:
            json.dump(beers, file, indent=4)
    elif file_type == '.xml':
        # Écrire en XML
        create_beer_xml(beers, output_path)

def random_brand():
    return random.choice(["Carlsberg", "Brewdog", "Heineken", "Guinness", "Budweiser"])

def random_name():
    return random.choice(["Imperial Stout", "Pale Ale", "Lager", "Pilsner", "Porter"])

def random_style():
    return random.choice(["Strong Ale", "Session IPA", "Wheat Beer", "Sour Ale", "Belgian Dubbel"])

def random_hop():
    return random.choice(["Millennium", "Cascade", "Galaxy", "Saaz", "Mosaic"])

def random_yeast():
    return random.choice(["1388 - Belgian Strong Ale", "1056 - American Ale", "WLP001 - California Ale", "S04 - English Ale", "W34/70 - Lager"])

def random_malts():
    return random.choice(["Victory", "Pilsner", "Munich", "Caramel", "Chocolate"])

def random_ibu():
    return f"{random.randint(20, 70)} IBU"

def random_alcohol():
    return f"{random.uniform(4.0, 10.0):.1f}%"

def random_blg():
    return f"{random.uniform(10.0, 20.0):.1f}°Blg"

# Chemins des sous-dossiers CSV, JSON, XML
csv_dir = '/home/stefen/data/bank/csv'
json_dir = '/home/stefen/data/bank/json'
xml_dir = '/home/stefen/data/bank/xml'

# Créer le dossier 'beer'...
beer_folder = '/home/stefen/data/beer'
os.makedirs(beer_folder, exist_ok=True)

# Traiter les fichiers et générer les données de bière
process_files(csv_dir, '.csv')
process_files(json_dir, '.json')
process_files(xml_dir, '.xml')
