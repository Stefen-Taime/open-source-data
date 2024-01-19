import os
import json
import csv
import xml.etree.ElementTree as ET
import random
import uuid
from datetime import datetime

# Fonctions pour générer des valeurs aléatoires pour les films
def random_genre():
    genres = [
        {'id': 18, 'name': 'Drama'}, 
        {'id': 16, 'name': 'Animation'}, 
        {'id': 878, 'name': 'Science Fiction'}, 
        {'id': 35, 'name': 'Comedy'},
        {'id': 10749, 'name': 'Romance'}, 
        {'id': 12, 'name': 'Adventure'}, 
        {'id': 80, 'name': 'Crime'}
    ]
    return random.sample(genres, random.randint(1, 3)) 

def random_production_company():
    companies = [
        {'name': 'D.A. Films', 'id': 6541},
        {'name': 'Tatsunoko Productions Company', 'id': 34037},
        {'name': 'Studio Ghibli', 'id': 34038},
        {'name': 'Warner Bros', 'id': 34039},
        {'name': 'Pixar Animation Studios', 'id': 34040}
    ]
    return random.sample(companies, random.randint(1, 2)) 

def random_production_country():
    countries = [
        {'iso_3166_1': 'FR', 'name': 'France'}, 
        {'iso_3166_1': 'JP', 'name': 'Japan'},
        {'iso_3166_1': 'US', 'name': 'United States'},
        {'iso_3166_1': 'GB', 'name': 'United Kingdom'},
        {'iso_3166_1': 'DE', 'name': 'Germany'}
    ]
    return random.sample(countries, random.randint(1, 2)) 
def random_language():
    # Retourne une langue aléatoire
    languages = ["fr", "ja", "en", "es", "de"]
    return random.choice(languages)

def random_overview():
    # Retourne une description fictive aléatoire
    overviews = [
        "This is a dramatic story of love and adventure.",
        "A thrilling journey of discovery unfolds in this exciting film.",
        "A comedic tale of mishaps and friendship.",
        "An intense drama about the challenges of life and relationships."
    ]
    return random.choice(overviews)

def random_popularity():
    # Génère un score de popularité aléatoire
    return round(random.uniform(0, 10), 6)

def random_release_date():
    year = random.randint(1980, 2020)
    month = random.randint(1, 12)
    day = random.randint(1, 28)
    return f"{year}-{month:02d}-{day:02d}"

def random_revenue():
    return float(random.randint(0, 1000000))

def random_status():
    return random.choice(["Released", "Post Production", "In Production"])

def random_title():
    return "Random Movie Title"

def random_vote():
    return round(random.uniform(0, 10), 1), random.randint(0, 1000)


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

def create_movies_xml(companies, file_path):
    root = ET.Element('Companies')
    for company in companies:
        company_elem = ET.SubElement(root, 'Computer')
        for key, val in company.items():
            child = ET.SubElement(company_elem, key)
            child.text = str(val)
    tree = ET.ElementTree(root)
    tree.write(file_path)


# Fonction pour écrire les données de film dans les fichiers correspondants
def write_movies_data(movies_data, movies_folder, file_type, original_filename):
    output_folder = os.path.join(movies_folder, file_type.strip('.'))
    os.makedirs(output_folder, exist_ok=True)
    output_path = os.path.join(output_folder, original_filename)

    if file_type == '.csv':
        with open(output_path, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=movies_data[0].keys())
            writer.writeheader()
            for movie in movies_data:
                writer.writerow(movie)
    elif file_type == '.json':
        with open(output_path, 'w') as file:
            json.dump(movies_data, file, indent=4)
    elif file_type == '.xml':
        create_movies_xml(movies_data, output_path)

# Fonction pour traiter tous les fichiers dans un dossier pour les films
def process_movies_files(directory, file_type, movies_folder):
    for filename in os.listdir(directory):
        if filename.endswith(file_type):
            file_path = os.path.join(directory, filename)
            if file_type == '.csv':
                records = read_csv_file(file_path)
            elif file_type == '.json':
                records = read_json_file(file_path)
            elif file_type == '.xml':
                records = read_xml_file(file_path)

            movies_list = []
            for record in records:
                vote_average, vote_count = random_vote()
                movie_data = {
                    "user_id": record['user_id'],
                    "adult": random.choice(["True", "False"]),
                    "belongs_to_collection": None,
                    "genres": json.dumps(random_genre()),
                    "id": str(uuid.uuid4()),
                    "imdb_id": f"tt{random.randint(1000000, 9999999)}",
                    "original_language": random_language(),
                    "original_title": random_title(),
                    "overview": random_overview(),
                    "popularity": random_popularity(),
                    "production_companies": json.dumps(random_production_company()),
                    "production_countries": json.dumps(random_production_country()),
                    "release_date": random_release_date(),
                    "revenue": random_revenue(),
                    "status": random_status(),
                    "title": random_title(),
                    "vote_average": vote_average,
                    "vote_count": vote_count,
                    "dt_current_timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }
                movies_list.append(movie_data)

            write_movies_data(movies_list, movies_folder, file_type, filename)

movies_folder = '/home/stefen/data/movies'
os.makedirs(movies_folder, exist_ok=True)

csv_dir = '/home/stefen/data/bank/csv'
json_dir = '/home/stefen/data/bank/json'
xml_dir = '/home/stefen/data/bank/xml'

# Traitement des fichiers
process_movies_files(csv_dir, '.csv', movies_folder)
process_movies_files(json_dir, '.json', movies_folder)
process_movies_files(xml_dir, '.xml', movies_folder)