import os
import json
import csv
import xml.etree.ElementTree as ET
import random
import uuid
from datetime import datetime
from faker import Faker

fake = Faker()

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

def get_user_ids_from_data(data):
    return {item['user_id'] for item in data}

def generate_random_user(user_id, credit_card_info, subscription_info):
    return {
        "id": random.randint(1000, 9999),
        "uid": user_id,
        "password": fake.password(),
        "first_name": fake.first_name(),
        "last_name": fake.last_name(),
        "username": fake.user_name(),
        "email": fake.email(),
        "avatar": fake.image_url(),
        "gender": random.choice(["Male", "Female", "Other"]),
        "phone_number": fake.phone_number(),
        "social_insurance_number": fake.ssn(),
        "date_of_birth": str(fake.date_of_birth()),
        "employment": {
            "title": fake.job(),
            "key_skill": "Teamwork"
        },
        "address": {
            "city": fake.city(),
            "street_name": fake.street_name(),
            "street_address": fake.street_address(),
            "zip_code": fake.zipcode(),
            "state": fake.state(),
            "country": fake.country(),
            "coordinates": {
                "lat": float(fake.latitude()),
                "lng": float(fake.longitude())
            }
        },
        "credit_card": credit_card_info,
        "subscription": subscription_info,
        "dt_current_timestamp": int(datetime.now().timestamp())
    }

def create_user_xml(users, file_path):
    root = ET.Element('Users')
    for user in users:
        user_elem = ET.SubElement(root, 'User')
        for key, val in user.items():
            child = ET.SubElement(user_elem, key)
            child.text = str(val)
    tree = ET.ElementTree(root)
    tree.write(file_path)

def write_user_data(users, user_folder, file_type, original_filename):
    output_folder = os.path.join(user_folder, file_type.strip('.'))
    os.makedirs(output_folder, exist_ok=True)
    output_path = os.path.join(output_folder, original_filename)

    if file_type == '.csv':
        with open(output_path, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=users[0].keys())
            writer.writeheader()
            for user in users:
                writer.writerow(user)
    elif file_type == '.json':
        with open(output_path, 'w') as file:
            json.dump(users, file, indent=4)
    elif file_type == '.xml':
        create_user_xml(users, output_path)

def get_data_from_folder(folder, read_function):
    data = []
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        data.extend(read_function(file_path))
    return data
# Lire les données de carte de crédit et d'abonnement
credit_card_csv_dir = '/home/stefen/data/credit_card/csv'
subscription_csv_dir = '/home/stefen/data/subscription/csv'

credit_card_data = get_data_from_folder(credit_card_csv_dir, read_csv_file)
subscription_data = get_data_from_folder(subscription_csv_dir, read_csv_file)

# Extraire les user_id uniques
user_ids = get_user_ids_from_data(credit_card_data + subscription_data)

# Générer les données d'utilisateur
user_folder = '/home/stefen/data/user'
os.makedirs(user_folder, exist_ok=True)

users = []
for user_id in user_ids:
    credit_card_info = next((item for item in credit_card_data if item["user_id"] == user_id), {})
    subscription_info = next((item for item in subscription_data if item["user_id"] == user_id), {})
    users.append(generate_random_user(user_id, credit_card_info, subscription_info))

# Écrire les données d'utilisateur
write_user_data(users, user_folder, '.csv', 'users.csv')
write_user_data(users, user_folder, '.json', 'users.json')
write_user_data(users, user_folder, '.xml', 'users.xml')