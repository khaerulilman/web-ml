# app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
from apriori_logic import apriori_model
from dataset_storage import get_dataset, add_transaction, update_transaction, delete_transaction

app = Flask(__name__)
CORS(app)

@app.route('/', methods=['GET'])
def home():
    return jsonify({'message': 'Flask API Apriori Tajwid is running!'}), 200

@app.route('/dataset', methods=['GET'])
def get_dataset_route():
    """Ambil semua dataset"""
    try:
        dataset = get_dataset()
        return jsonify(dataset), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/dataset', methods=['POST'])
def add_dataset():
    """Tambah transaksi baru"""
    try:
        data = request.json
        if not data or not isinstance(data, list):
            return jsonify({'error': 'Data harus berupa list'}), 400
        
        # Filter data kosong
        filtered_data = [item.strip() for item in data if item.strip()]
        if not filtered_data:
            return jsonify({'error': 'Data tidak boleh kosong'}), 400
            
        add_transaction(filtered_data)
        return jsonify({'message': 'Transaksi berhasil ditambahkan', 'data': filtered_data}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/dataset/<int:index>', methods=['PUT'])
def update_dataset(index):
    """Update transaksi berdasarkan index"""
    try:
        data = request.json
        if not data or not isinstance(data, list):
            return jsonify({'error': 'Data harus berupa list'}), 400
        
        # Filter data kosong
        filtered_data = [item.strip() for item in data if item.strip()]
        if not filtered_data:
            return jsonify({'error': 'Data tidak boleh kosong'}), 400
        
        if update_transaction(index, filtered_data):
            return jsonify({'message': 'Transaksi berhasil diupdate', 'data': filtered_data}), 200
        else:
            return jsonify({'error': 'Index tidak valid'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/dataset/<int:index>', methods=['DELETE'])
def delete_dataset(index):
    """Hapus transaksi berdasarkan index"""
    try:
        if delete_transaction(index):
            return jsonify({'message': 'Transaksi berhasil dihapus'}), 200
        else:
            return jsonify({'error': 'Index tidak valid'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/rules', methods=['POST'])
def generate_rules():
    """Generate aturan asosiasi"""
    try:
        req = request.json
        min_support = req.get("min_support", 0.3)
        min_confidence = req.get("min_confidence", 0.6)
        
        dataset = get_dataset()
        if not dataset:
            return jsonify({'error': 'Dataset kosong'}), 400
        
        rules_df = apriori_model(dataset, min_support, min_confidence)
        
        if rules_df.empty:
            return jsonify([]), 200
        
        rules = rules_df.to_dict(orient='records')
        
        # Konversi frozenset ke list untuk JSON serialization
        for rule in rules:
            rule['antecedents'] = list(rule['antecedents'])
            rule['consequents'] = list(rule['consequents'])
        
        return jsonify(rules), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)