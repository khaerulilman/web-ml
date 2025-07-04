# dataset_storage.py
import json
import os

# File untuk menyimpan dataset
DATASET_FILE = "dataset.json"

def load_dataset():
    """Load dataset dari file JSON"""
    if os.path.exists(DATASET_FILE):
        try:
            with open(DATASET_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading dataset: {e}")
            return []
    return []

def save_dataset(dataset):
    """Simpan dataset ke file JSON"""
    try:
        with open(DATASET_FILE, 'w', encoding='utf-8') as f:
            json.dump(dataset, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        print(f"Error saving dataset: {e}")
        return False

# Load dataset saat pertama kali import
DATASET = load_dataset()

def get_dataset():
    """Ambil dataset"""
    return DATASET

def add_transaction(transaction):
    """Tambah transaksi baru"""
    global DATASET
    DATASET.append(transaction)
    save_dataset(DATASET)
    return True

def update_transaction(index, new_transaction):
    """Update transaksi berdasarkan index"""
    global DATASET
    if 0 <= index < len(DATASET):
        DATASET[index] = new_transaction
        save_dataset(DATASET)
        return True
    return False

def delete_transaction(index):
    """Hapus transaksi berdasarkan index"""
    global DATASET
    if 0 <= index < len(DATASET):
        del DATASET[index]
        save_dataset(DATASET)
        return True
    return False

def clear_dataset():
    """Hapus semua data"""
    global DATASET
    DATASET = []
    save_dataset(DATASET)
    return True