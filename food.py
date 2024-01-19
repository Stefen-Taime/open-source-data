import os
import json
import csv
import xml.etree.ElementTree as ET
import random
import uuid
from datetime import datetime

# Fonctions pour générer des valeurs aléatoires pour les plats
def random_dish():
    dishes = {
        "Som Tam": "Granny Smith apples mixed with brown sugar and butter filling, in a flaky all-butter crust, with ice cream.",
        "Pizza": "Smoked salmon, poached eggs, diced red onions and Hollandaise sauce on an English muffin. With a side of roasted potatoes.",
        "Pork Sausage Roll": "Two buttermilk waffles, topped with whipped cream and maple syrup, a side of two eggs served any style, and your choice of smoked bacon or smoked ham.",
        "Cheeseburger": "Three eggs with cilantro, tomatoes, onions, avocados and melted Emmental cheese. With a side of roasted potatoes, and your choice of toast or croissant."
    }
    dish = random.choice(list(dishes.keys()))
    description = dishes[dish]
    return dish, description

def random_description():
    descriptions = {
        "Som Tam": "Granny Smith apples mixed with brown sugar and butter filling, in a flaky all-butter crust, with ice cream.",
        "Pizza": "Smoked salmon, poached eggs, diced red onions and Hollandaise sauce on an English muffin. With a side of roasted potatoes.",
        "Pork Sausage Roll": "Two buttermilk waffles, topped with whipped cream and maple syrup, a side of two eggs served any style, and your choice of smoked bacon or smoked ham.",
        "Cheeseburger": "Three eggs with cilantro, tomatoes, onions, avocados and melted Emmental cheese. With a side of roasted potatoes, and your choice of toast or croissant."
        # Ajoutez d'autres descriptions si nécessaire
    }
    dish = random.choice(list(descriptions.keys()))
    return dish, descriptions[dish]

def random_ingredient():
    return random.choice(["Feijoa", "Curry Powder", "Pinto Beans", "Tomato"])

def random_measurement():
    return random.choice(["1/4 pint", "1/2 gallon", "1/2 cup", "2 tablespoons"])


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

def create_food_xml(companies, file_path):
    root = ET.Element('Companies')
    for company in companies:
        company_elem = ET.SubElement(root, 'Computer')
        for key, val in company.items():
            child = ET.SubElement(company_elem, key)
            child.text = str(val)
    tree = ET.ElementTree(root)
    tree.write(file_path)


# Fonction pour écrire les données de plat dans les fichiers correspondants
def write_food_data(foods, food_folder, file_type, original_filename):
    output_folder = os.path.join(food_folder, file_type.strip('.'))
    os.makedirs(output_folder, exist_ok=True)
    output_path = os.path.join(output_folder, original_filename)

    if file_type == '.csv':
        with open(output_path, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=foods[0].keys())
            writer.writeheader()
            for food in foods:
                writer.writerow(food)
    elif file_type == '.json':
        with open(output_path, 'w') as file:
            json.dump(foods, file, indent=4)
    elif file_type == '.xml':
        create_food_xml(foods, output_path)

# Fonction pour traiter tous les fichiers dans un dossier pour les plats
def process_food_files(directory, file_type, food_folder):
    for filename in os.listdir(directory):
        if filename.endswith(file_type):
            file_path = os.path.join(directory, filename)
            if file_type == '.csv':
                records = read_csv_file(file_path)
            elif file_type == '.json':
                records = read_json_file(file_path)
            elif file_type == '.xml':
                records = read_xml_file(file_path)

            foods = []
            for record in records:
                dish, description = random_dish()
                food_data = {
                    "id": random.randint(1000, 9999),
                    "uid": str(uuid.uuid4()),
                    "dish": dish,
                    "description": description,
                    "ingredient": random_ingredient(),
                    "measurement": random_measurement(),
                    "user_id": record['user_id'],
                    "dt_current_timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }
                foods.append(food_data)

            write_food_data(foods, food_folder, file_type, filename)

food_folder = '/home/stefen/data/food'
os.makedirs(food_folder, exist_ok=True)

csv_dir = '/home/stefen/data/bank/csv'
json_dir = '/home/stefen/data/bank/json'
xml_dir = '/home/stefen/data/bank/xml'

# Traitement des fichiers
process_food_files(csv_dir, '.csv', food_folder)
process_food_files(json_dir, '.json', food_folder)
process_food_files(xml_dir, '.xml', food_folder)