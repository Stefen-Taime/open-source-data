import os
import json
import csv
import xml.etree.ElementTree as ET
import random
import uuid
from datetime import datetime

# Fonctions pour générer des valeurs aléatoires pour les abonnements
def random_plan():
    plans = ["Standard", "Basic", "Platinum", "Gold", "Bronze"]
    return random.choice(plans)

def random_status():
    statuses = ["Active", "Idle", "Blocked", "Cancelled"]
    return random.choice(statuses)

def random_payment_method():
    methods = ["Google Pay", "Credit Card", "Paypal", "Bitcoins", "Money Transfer", "Alipay"]
    return random.choice(methods)

def random_subscription_term():
    terms = ["Weekly", "Monthly", "Yearly", "Lifetime", "Quinquennal"]
    return random.choice(terms)

def random_payment_term():
    terms = ["Full Subscription", "Monthly Payment", "Payment in Advance", "Pay per Use"]
    return random.choice(terms)
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


# Fonction pour créer un fichier XML pour les données d'abonnement
def create_subscription_xml(subscriptions, file_path):
    root = ET.Element('Subscriptions')
    for subscription in subscriptions:
        subscription_elem = ET.SubElement(root, 'Subscription')
        for key, val in subscription.items():
            child = ET.SubElement(subscription_elem, key)
            child.text = str(val)
    tree = ET.ElementTree(root)
    tree.write(file_path)

# Fonction pour écrire les données d'abonnement dans les fichiers correspondants
def write_subscription_data(subscriptions, subscription_folder, file_type, original_filename):
    output_folder = os.path.join(subscription_folder, file_type.strip('.'))
    os.makedirs(output_folder, exist_ok=True)
    output_path = os.path.join(output_folder, original_filename)

    if file_type == '.csv':
        with open(output_path, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=subscriptions[0].keys())
            writer.writeheader()
            for subscription in subscriptions:
                writer.writerow(subscription)
    elif file_type == '.json':
        with open(output_path, 'w') as file:
            json.dump(subscriptions, file, indent=4)
    elif file_type == '.xml':
        create_subscription_xml(subscriptions, output_path)

# Fonction pour traiter tous les fichiers dans un dossier pour les abonnements
def process_subscription_files(directory, file_type, subscription_folder):
    for filename in os.listdir(directory):
        if filename.endswith(file_type):
            file_path = os.path.join(directory, filename)
            if file_type == '.csv':
                records = read_csv_file(file_path)
            elif file_type == '.json':
                records = read_json_file(file_path)
            elif file_type == '.xml':
                records = read_xml_file(file_path)

            subscriptions = []
            for record in records:
                subscription_data = {
                    "id": record["id"],
                    "uid": str(uuid.uuid4()),
                    "plan": random_plan(),
                    "status": random_status(),
                    "payment_method": random_payment_method(),
                    "subscription_term": random_subscription_term(),
                    "payment_term": random_payment_term(),
                    "user_id": record['user_id'],
                    "dt_current_timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }
                subscriptions.append(subscription_data)

            write_subscription_data(subscriptions, subscription_folder, file_type, filename)

subscription_folder = '/home/stefen/data/subscription'
os.makedirs(subscription_folder, exist_ok=True)

subscription_csv_dir = '/home/stefen/data/stripe/csv'
subscription_json_dir = '/home/stefen/data/stripe/json'
subscription_xml_dir = '/home/stefen/data/stripe/xml'

# Traitement des fichiers
process_subscription_files(subscription_csv_dir, '.csv', subscription_folder)
process_subscription_files(subscription_json_dir, '.json', subscription_folder)
process_subscription_files(subscription_xml_dir, '.xml', subscription_folder)
