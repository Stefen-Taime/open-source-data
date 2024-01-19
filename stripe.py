import os
import json
import csv
import xml.etree.ElementTree as ET
import random
import uuid
from datetime import datetime

# Fonctions pour générer des valeurs aléatoires pour les transactions Stripe
def random_valid_card():
    valid_cards = ["6011000990139424", "6011111111111117", "5105105105105100"]
    return random.choice(valid_cards)

def random_token():
    tokens = ["tok_visa", "tok_mastercard", "tok_discover"]
    return random.choice(tokens)

def random_invalid_card():
    invalid_cards = ["4000000000000044", "4000000000000101", "4000000000000028"]
    return random.choice(invalid_cards)

def random_month():
    return random.choice(["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"])

def random_year():
    current_year = datetime.now().year
    return str(random.randint(current_year, current_year + 10))

def random_ccv():
    return str(random.randint(100, 999))

def random_ccv_amex():
    return str(random.randint(1000, 9999))

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


# Fonction pour créer un fichier XML pour les données Stripe
def create_stripe_xml(transactions, file_path):
    root = ET.Element('Transactions')
    for transaction in transactions:
        transaction_elem = ET.SubElement(root, 'Transaction')
        for key, val in transaction.items():
            child = ET.SubElement(transaction_elem, key)
            child.text = str(val)
    tree = ET.ElementTree(root)
    tree.write(file_path)

# Fonction pour écrire les données Stripe dans les fichiers correspondants
def write_stripe_data(transactions, stripe_folder, file_type, original_filename):
    output_folder = os.path.join(stripe_folder, file_type.strip('.'))
    os.makedirs(output_folder, exist_ok=True)
    output_path = os.path.join(output_folder, original_filename)

    if file_type == '.csv':
        with open(output_path, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=transactions[0].keys())
            writer.writeheader()
            for transaction in transactions:
                writer.writerow(transaction)
    elif file_type == '.json':
        with open(output_path, 'w') as file:
            json.dump(transactions, file, indent=4)
    elif file_type == '.xml':
        create_stripe_xml(transactions, output_path)

# Fonction pour traiter tous les fichiers dans un dossier pour les transactions Stripe
def process_stripe_files(directory, file_type, stripe_folder):
    for filename in os.listdir(directory):
        if filename.endswith(file_type):
            file_path = os.path.join(directory, filename)
            if file_type == '.csv':
                records = read_csv_file(file_path)
            elif file_type == '.json':
                records = read_json_file(file_path)
            elif file_type == '.xml':
                records = read_xml_file(file_path)

            transactions = []
            for record in records:
                transaction_data = {
                    "id": random.randint(1000, 9999),
                    "uid": str(uuid.uuid4()),
                    "valid_card": record['credit_card_number'],
                    "token": random_token(),
                    "invalid_card": random_invalid_card(),
                    "month": record['credit_card_expiry_date'].split("-")[1],
                    "year": record['credit_card_expiry_date'].split("-")[0],
                    "ccv": random_ccv(),
                    "ccv_amex": random_ccv_amex(),
                    "user_id": record['user_id'],
                    "dt_current_timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }
                transactions.append(transaction_data)

            write_stripe_data(transactions, stripe_folder, file_type, filename)

stripe_folder = '/home/stefen/data/stripe'
os.makedirs(stripe_folder, exist_ok=True)

credit_card_csv_dir = '/home/stefen/data/credit_card/csv'
credit_card_json_dir = '/home/stefen/data/credit_card/json'
credit_card_xml_dir = '/home/stefen/data/credit_card/xml'

# Traitement des fichiers
process_stripe_files(credit_card_csv_dir, '.csv', stripe_folder)
process_stripe_files(credit_card_json_dir, '.json', stripe_folder)
process_stripe_files(credit_card_xml_dir, '.xml', stripe_folder)