import os
import json
import csv
import xml.etree.ElementTree as ET
import random
import uuid
from datetime import datetime

# Fonctions pour générer des valeurs aléatoires pour les produits
def random_product_id():
    return random.randint(1000, 9999)

def random_color():
    return random.choice(["red", "green", "blue", "yellow", "purple"])

def random_department():
    return random.choice(["Electronics", "Fashion", "Footwear", "Audio", "Kitchen"])

def random_material():
    return random.choice(["Plastic", "Metal", "Leather", "Cotton", "Rubber"])

def random_product_name():
    return random.choice(["Smart TV", "Leather Wallet", "Running Shoes", "Bluetooth Headphones", "Coffee Maker"])

def random_price():
    return round(random.uniform(50.0, 500.0), 2)

def random_price_string(price):
    return "{:.2f}".format(price)

def random_discount_code():
    return "DISCOUNT" + str(random.randint(10, 99))

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

# Fonction pour créer un fichier XML pour les produits
def create_product_xml(products, file_path):
    root = ET.Element('Products')
    for product in products:
        product_elem = ET.SubElement(root, 'Product')
        for key, val in product.items():
            child = ET.SubElement(product_elem, key)
            child.text = str(val)
    tree = ET.ElementTree(root)
    tree.write(file_path)

# Fonction pour écrire les données de produit dans les fichiers correspondants
def write_product_data(products, product_folder, file_type, original_filename):
    output_folder = os.path.join(product_folder, file_type.strip('.'))
    os.makedirs(output_folder, exist_ok=True)
    output_path = os.path.join(output_folder, original_filename)

    if file_type == '.csv':
        with open(output_path, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=products[0].keys())
            writer.writeheader()
            for product in products:
                writer.writerow(product)
    elif file_type == '.json':
        with open(output_path, 'w') as file:
            json.dump(products, file, indent=4)
    elif file_type == '.xml':
        create_product_xml(products, output_path)

# Fonction pour traiter tous les fichiers dans un dossier pour les produits
def process_product_files(directory, file_type, product_folder):
    for filename in os.listdir(directory):
        if filename.endswith(file_type):
            file_path = os.path.join(directory, filename)
            if file_type == '.csv':
                records = read_csv_file(file_path)
            elif file_type == '.json':
                records = read_json_file(file_path)
            elif file_type == '.xml':
                records = read_xml_file(file_path)

            products = []
            for record in records:
                price = random_price()
                product_data = {
                    "id": random_product_id(),
                    "color": random_color(),
                    "department": random_department(),
                    "material": random_material(),
                    "product_name": random_product_name(),
                    "price": price,
                    "price_string": random_price_string(price),
                    "promo_code": random_discount_code(),
                    "user_id": record['user_id'],  # Utiliser le user_id de l'enregistrement original
                    "dt_current_timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }
                products.append(product_data)

            write_product_data(products, product_folder, file_type, filename)

product_folder = '/home/stefen/data/commerce'
os.makedirs(product_folder, exist_ok=True)

csv_dir = '/home/stefen/data/bank/csv'
json_dir = '/home/stefen/data/bank/json'
xml_dir = '/home/stefen/data/bank/xml'

# Traitement des fichiers
process_product_files(csv_dir, '.csv', product_folder)
process_product_files(json_dir, '.json', product_folder)
process_product_files(xml_dir, '.xml', product_folder)