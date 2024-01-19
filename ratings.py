import os
import json
import csv
import random
import time
from datetime import datetime
import xml.etree.ElementTree as ET

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

# Fonction pour générer une note aléatoire
def random_rating():
    return round(random.uniform(0.5, 5.0), 1)  # Notation entre 0.5 et 5.0

# Fonction pour créer un fichier XML pour les données de notation
def create_ratings_xml(ratings_data, file_path):
    root = ET.Element('Ratings')
    for rating in ratings_data:
        rating_elem = ET.SubElement(root, 'Rating')
        for key, val in rating.items():
            child = ET.SubElement(rating_elem, key)
            child.text = str(val)
    tree = ET.ElementTree(root)
    tree.write(file_path)

# Fonction pour écrire les données de notation dans les fichiers correspondants
def write_ratings_data(ratings_data, ratings_folder, file_type, original_filename):
    output_folder = os.path.join(ratings_folder, file_type.strip('.'))
    os.makedirs(output_folder, exist_ok=True)
    output_path = os.path.join(output_folder, original_filename)

    if file_type == '.csv':
        with open(output_path, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=ratings_data[0].keys())
            writer.writeheader()
            for rating in ratings_data:
                writer.writerow(rating)
    elif file_type == '.json':
        with open(output_path, 'w') as file:
            json.dump(ratings_data, file, indent=4)
    elif file_type == '.xml':
        create_ratings_xml(ratings_data, output_path)

# Fonction pour lire les données de films et générer des données de notation
def create_ratings_data(movies_folders, ratings_folder):
    for folder, file_type in movies_folders:
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            movies_data = []
            if file_type == '.csv':
                movies_data = read_csv_file(file_path)
            elif file_type == '.json':
                movies_data = read_json_file(file_path)
            elif file_type == '.xml':
                movies_data = read_xml_file(file_path)

            ratings_list = []
            for movie in movies_data:
                rating_data = {
                    "user_id": movie["user_id"],
                    "movieid": movie["id"],
                    "rating": random_rating(),
                    "timestamp": int(time.mktime(datetime.now().timetuple())),
                    "dt_current_timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }
                ratings_list.append(rating_data)

            # Créer un fichier de notation pour chaque fichier de film
            output_filename = "ratings_" + os.path.basename(filename)
            write_ratings_data(ratings_list, ratings_folder, file_type, output_filename)

# Chemins vers les dossiers contenant les données de films
csv_dir = '/home/stefen/data/movies/csv'
json_dir = '/home/stefen/data/movies/json'
xml_dir = '/home/stefen/data/movies/xml'

# Liste des dossiers contenant les données de films avec leur type de fichier correspondant
movies_folders = [
    (csv_dir, '.csv'),
    (json_dir, '.json'),
    (xml_dir, '.xml')
]

# Chemin vers le dossier pour les données de notation
ratings_folder = '/home/stefen/data/ratings'
os.makedirs(ratings_folder, exist_ok=True)

# Créer et écrire des données de notation
create_ratings_data(movies_folders, ratings_folder)
