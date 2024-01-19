import os
import json
import csv
import random
import string
import uuid
from datetime import datetime
import xml.etree.ElementTree as ET

# Liste de noms de banques fictifs
bank_names = [
    "Global Trust Bank", "Silverline Financial", "Oceanic Capital", "Liberty Banking Corp", "Pinnacle Funds",
    "Banque du Soleil", "Finance Royale", "Banco del Futuro", "Zhongxin Jinrong"
]

# Fonctions auxiliaires pour générer des données aléatoires
def random_uuid():
    return str(uuid.uuid4())

def random_number(length=10):
    numbers = string.digits
    return ''.join(random.choice(numbers) for i in range(length))

def random_iban():
    return 'IBAN' + random_number(20)

def random_swift_bic():
    return 'SWIFT' + ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(8))

# Fonction pour créer le XML
def create_xml(records, file_path):
    root = ET.Element('Records')
    for record in records:
        rec_elem = ET.SubElement(root, 'Record')
        for key, val in record.items():
            child = ET.SubElement(rec_elem, key)
            child.text = str(val)
    tree = ET.ElementTree(root)
    tree.write(file_path)

# Chemin de base modifié
base_dir = '/home/stefen/data/bank' 

# Dossiers pour les fichiers CSV, JSON et XML
csv_dir = os.path.join(base_dir, 'csv')
json_dir = os.path.join(base_dir, 'json')
xml_dir = os.path.join(base_dir, 'xml')

# Création des dossiers s'ils n'existent pas
os.makedirs(csv_dir, exist_ok=True)
os.makedirs(json_dir, exist_ok=True)
os.makedirs(xml_dir, exist_ok=True)

# Obtention de la date actuelle pour nommer les fichiers
current_date = datetime.now().strftime('%Y%m%d')

# Création et sauvegarde des fichiers
for file_id in range(1, 6):
    # Générer 100 enregistrements uniques pour chaque fichier CSV, JSON et XML
    csv_records, json_records, xml_records = [], [], []
    # Dans la boucle de création des enregistrements :
    for i in range(100):
        common_record = {
            "uid": random_uuid(),
            "account_number": random_number(),
            "iban": random_iban(),
            "bank_name": random.choice(bank_names),
            "routing_number": random_number(),
            "swift_bic": random_swift_bic(),
            "user_id": str(uuid.uuid4()),  # Utilisation de UUID pour garantir l'unicité
            "dt_current_timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        csv_records.append({"id": i + (file_id - 1) * 300, **common_record})
        json_records.append({"id": i + 100 + (file_id - 1) * 300, **common_record})
        xml_records.append({"id": i + 200 + (file_id - 1) * 300, **common_record})

    # Noms de fichiers basés sur le dossier, le sous-dossier et la date actuelle
    csv_file_name = f'csv_bank_{current_date}_{file_id}.csv'
    json_file_name = f'json_bank_{current_date}_{file_id}.json'
    xml_file_name = f'xml_bank_{current_date}_{file_id}.xml'

    # Chemins complets des fichiers
    csv_file_path = os.path.join(csv_dir, csv_file_name)
    json_file_path = os.path.join(json_dir, json_file_name)
    xml_file_path = os.path.join(xml_dir, xml_file_name)
    
    # Sauvegarder en CSV
    with open(csv_file_path, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=csv_records[0].keys())
        writer.writeheader()
        writer.writerows(csv_records)

    # Sauvegarder en JSON
    with open(json_file_path, 'w') as file:
        json.dump(json_records, file, indent=4)

    # Sauvegarder en XML
    create_xml(xml_records, xml_file_path)
