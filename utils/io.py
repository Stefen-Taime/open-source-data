"""Shared I/O functions for reading and writing CSV, JSON, and XML files."""

import os
import csv
import json
import xml.etree.ElementTree as ET


# ---------------------------------------------------------------------------
# Readers
# ---------------------------------------------------------------------------

def read_csv(file_path: str) -> list[dict]:
    """Read a CSV file and return a list of dicts."""
    with open(file_path, mode="r", newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def read_json(file_path: str) -> list[dict]:
    """Read a JSON file and return a list of dicts."""
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


def read_xml(file_path: str) -> list[dict]:
    """Read an XML file and return a list of dicts (one per child element)."""
    tree = ET.parse(file_path)
    root = tree.getroot()
    records = []
    for record in root:
        record_data = {child.tag: child.text for child in record}
        records.append(record_data)
    return records


def read_file(file_path: str) -> list[dict]:
    """Auto-detect format by extension and read the file."""
    ext = os.path.splitext(file_path)[1].lower()
    readers = {".csv": read_csv, ".json": read_json, ".xml": read_xml}
    reader = readers.get(ext)
    if reader is None:
        raise ValueError(f"Unsupported file format: {ext}")
    return reader(file_path)


def read_all_from_folder(folder: str) -> list[dict]:
    """Read every supported file in *folder* and return a merged list."""
    data = []
    for filename in sorted(os.listdir(folder)):
        ext = os.path.splitext(filename)[1].lower()
        if ext in (".csv", ".json", ".xml"):
            data.extend(read_file(os.path.join(folder, filename)))
    return data


# ---------------------------------------------------------------------------
# Writers
# ---------------------------------------------------------------------------

def write_csv(records: list[dict], file_path: str) -> None:
    """Write a list of dicts to a CSV file."""
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=records[0].keys())
        writer.writeheader()
        writer.writerows(records)


def write_json(records: list[dict], file_path: str) -> None:
    """Write a list of dicts to a JSON file."""
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(records, f, indent=4, ensure_ascii=False)


def write_xml(records: list[dict], file_path: str,
              root_tag: str = "Records", item_tag: str = "Record") -> None:
    """Write a list of dicts to an XML file with proper element names."""
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    root = ET.Element(root_tag)
    for record in records:
        item = ET.SubElement(root, item_tag)
        for key, val in record.items():
            child = ET.SubElement(item, key)
            child.text = str(val)
    tree = ET.ElementTree(root)
    ET.indent(tree, space="  ")
    tree.write(file_path, encoding="unicode", xml_declaration=True)


def write_data(records: list[dict], output_dir: str, category: str,
               file_index: int, date_str: str,
               root_tag: str = "Records", item_tag: str = "Record") -> None:
    """Write records to CSV, JSON, and XML in the standard directory layout.

    Creates files like:
        output_dir/csv/csv_{category}_{date_str}_{file_index}.csv
        output_dir/json/json_{category}_{date_str}_{file_index}.json
        output_dir/xml/xml_{category}_{date_str}_{file_index}.xml
    """
    for fmt, writer, ext in [
        ("csv", write_csv, "csv"),
        ("json", write_json, "json"),
        ("xml", lambda r, p: write_xml(r, p, root_tag, item_tag), "xml"),
    ]:
        filename = f"{fmt}_{category}_{date_str}_{file_index}.{ext}"
        file_path = os.path.join(output_dir, fmt, filename)
        writer(records, file_path)
