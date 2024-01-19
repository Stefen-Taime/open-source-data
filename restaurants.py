import os
import json
import csv
import xml.etree.ElementTree as ET
import random
import uuid
from datetime import datetime

# Fonctions pour générer des valeurs aléatoires pour les restaurants
def random_restaurant_name():
    names = ["Sweet Box", "66 BBQ", "Café Delight", "Ocean View", "Mountain Retreat"]
    return random.choice(names)

def random_restaurant_type():
    types = ["Bar", "Café", "Fast Food", "Fine Dining", "Bistro"]
    return random.choice(types)

def random_description():
    descriptions = [
        "A cozy place with home-style cooking.",
        "Elegant dining with a panoramic ocean view.",
        "Fast and delicious meals for the on-the-go customer.",
        "A perfect place for a romantic evening.",
        "Fresh and healthy food served in a comfortable setting."
    ]
    return random.choice(descriptions)

def random_review():
    reviews = [
        "Excellent food and friendly service!",
        "A bit pricey but totally worth it.",
        "Not the best experience, but the food was okay.",
        "Loved the ambience and the dessert menu.",
        "Great location, but the service could be better."
    ]
    return random.choice(reviews)

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


# Fonction pour créer un fichier XML pour les données de restaurant
def create_restaurant_xml(restaurants, file_path):
    root = ET.Element('Restaurants')
    for restaurant in restaurants:
        restaurant_elem = ET.SubElement(root, 'Restaurant')
        for key, val in restaurant.items():
            child = ET.SubElement(restaurant_elem, key)
            child.text = str(val)
    tree = ET.ElementTree(root)
    tree.write(file_path)

# Fonction pour écrire les données de restaurant dans les fichiers correspondants
def write_restaurant_data(restaurants, restaurant_folder, file_type, original_filename):
    output_folder = os.path.join(restaurant_folder, file_type.strip('.'))
    os.makedirs(output_folder, exist_ok=True)
    output_path = os.path.join(output_folder, original_filename)

    if file_type == '.csv':
        with open(output_path, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=restaurants[0].keys())
            writer.writeheader()
            for restaurant in restaurants:
                writer.writerow(restaurant)
    elif file_type == '.json':
        with open(output_path, 'w') as file:
            json.dump(restaurants, file, indent=4)
    elif file_type == '.xml':
        create_restaurant_xml(restaurants, output_path)

# Fonction pour traiter tous les fichiers dans un dossier pour les restaurants
def process_restaurant_files(directory, file_type, restaurant_folder):
    for filename in os.listdir(directory):
        if filename.endswith(file_type):
            file_path = os.path.join(directory, filename)
            if file_type == '.csv':
                records = read_csv_file(file_path)
            elif file_type == '.json':
                records = read_json_file(file_path)
            elif file_type == '.xml':
                records = read_xml_file(file_path)

            restaurants = []
            for record in records:
                restaurant_data = {
                    "id": random.randint(1000, 9999),
                    "uid": str(uuid.uuid4()),
                    "name": random_restaurant_name(),
                    "type": random_restaurant_type(),
                    "description": random_description(),
                    "review": random_review(),
                    "user_id": record['user_id'],
                    "dt_current_timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }
                restaurants.append(restaurant_data)

            write_restaurant_data(restaurants, restaurant_folder, file_type, filename)

restaurant_folder = '/home/stefen/data/restaurant'
os.makedirs(restaurant_folder, exist_ok=True)

csv_dir = '/home/stefen/data/bank/csv'
json_dir = '/home/stefen/data/bank/json'
xml_dir = '/home/stefen/data/bank/xml'

# Traitement des fichiers
process_restaurant_files(csv_dir, '.csv', restaurant_folder)
process_restaurant_files(json_dir, '.json', restaurant_folder)
process_restaurant_files(xml_dir, '.xml', restaurant_folder)
