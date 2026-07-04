from flask import Flask, request, jsonify, send_file
import pandas as pd
import os

app = Flask(__name__)

# 1. Load the database safely
try:
    base_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_dir, 'medicines.xlsx')
    
    df = pd.read_excel(file_path)
    df.columns = df.columns.str.strip()
except Exception as e:
    df = pd.DataFrame()
    print(f"Error loading DB: {e}")

# --- NEW: Serve the User Interface ---
@app.route('/')
def home():
    # Go up one folder from 'api' to find your index.html file
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    html_path = os.path.join(root_dir, 'index.html')
    return send_file(html_path)

# 2. Database Search Endpoint
@app.route('/api/search', methods=['GET'])
def search_med():
    query = request.args.get('q', '').lower()
    
    if df.empty:
        return jsonify({"status": "error", "message": "Database kosong."})
        
    filtered = df[
        df['Nama Generik'].astype(str).str.lower().str.contains(query, na=False) | 
        df['Jenama'].astype(str).str.lower().str.contains(query, na=False)
    ]
    
    results = filtered.head(5).to_dict(orient='records')
    return jsonify({"status": "success", "results": results})

# 3. Innova-thon "Mock" Camera Scanner Endpoint
@app.route('/api/scan', methods=['POST'])
def scan_image():
    return jsonify({
        "status": "success", 
        "scanned_text": "Paracetamol"
    })
