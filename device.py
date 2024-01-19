import os
import json
import csv
import xml.etree.ElementTree as ET
import random
import uuid
from datetime import datetime

def random_build_number():
    return random.randint(50, 500)

def random_serial_number():
    return ''.join(random.choices('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=16))

def random_version():
    return random.randint(100, 1000)

def random_device():
    manufacturers = {
        "Apple": {"models": ["iPhone 3GS", "iPhone X", "iPhone 11"], "platform": "iOS"},
        "Samsung": {"models": ["Galaxy S10", "Galaxy Note 10"], "platform": "Android"},
        "Google": {"models": ["Pixel 4", "Pixel 5"], "platform": "Android"},
        "HP": {"models": ["EliteBook", "ProBook"], "platform": "Windows"},
        "ASUS": {"models": ["ZenBook", "VivoBook"], "platform": "Windows"}
        # Ajoutez d'autres marques et modèles si nécessaire
    }

    manufacturer = random.choice(list(manufacturers.keys()))
    model = random.choice(manufacturers[manufacturer]["models"])
    platform = manufacturers[manufacturer]["platform"]

    return manufacturer, model, platform

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

def create_device_xml(devices, file_path):
    root = ET.Element('Devices')
    for device in devices:
        device_elem = ET.SubElement(root, 'Device')
        for key, val in device.items():
            child = ET.SubElement(device_elem, key)
            child.text = str(val)
    tree = ET.ElementTree(root)
    tree.write(file_path)

def write_device_data(devices, device_folder, file_type, original_filename):
    output_folder = os.path.join(device_folder, file_type.strip('.'))
    os.makedirs(output_folder, exist_ok=True)
    output_path = os.path.join(output_folder, original_filename)

    if file_type == '.csv':
        with open(output_path, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=devices[0].keys())
            writer.writeheader()
            for device in devices:
                writer.writerow(device)
    elif file_type == '.json':
        with open(output_path, 'w') as file:
            json.dump(devices, file, indent=4)
    elif file_type == '.xml':
        create_device_xml(devices, output_path)

def process_device_files(directory, file_type, device_folder):
    for filename in os.listdir(directory):
        if filename.endswith(file_type):
            file_path = os.path.join(directory, filename)
            if file_type == '.csv':
                records = read_csv_file(file_path)
            elif file_type == '.json':
                records = read_json_file(file_path)
            elif file_type == '.xml':
                records = read_xml_file(file_path)

            devices = []
            for record in records:
                manufacturer, model, platform = random_device()
                device_data = {
                    "id": random.randint(1000, 9999),
                    "uid": str(uuid.uuid4()),
                    "build_number": random_build_number(),
                    "manufacturer": manufacturer,
                    "model": model,
                    "platform": platform,
                    "serial_number": random_serial_number(),
                    "version": random_version(),
                    "user_id": record['user_id'],
                    "dt_current_timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }
                devices.append(device_data)

            write_device_data(devices, device_folder, file_type, filename)

device_folder = '/home/stefen/data/device'
os.makedirs(device_folder, exist_ok=True)

csv_dir = '/home/stefen/data/bank/csv'
json_dir = '/home/stefen/data/bank/json'
xml_dir = '/home/stefen/data/bank/xml'

process_device_files(csv_dir, '.csv', device_folder)
process_device_files(json_dir, '.json', device_folder)
process_device_files(xml_dir, '.xml', device_folder)
