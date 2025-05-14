import os
import json
import sqlite3
from flask import Flask, jsonify, render_template
app = Flask(__name__)
DB_PATH = os.path.join(os.path.dirname(__file__), 'templates.db')
@app.route('/')
def home():
    return render_template('index.html')  
@app.route('/templates', methods=['GET'])
def get_templates():
    try:
        print(f"[INFO] DB path: {DB_PATH}")
        if not os.path.exists(DB_PATH):
            print("[ERROR] templates.db file not found!")
            return jsonify({'error': 'Database file not found'}), 500

        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('SELECT form_name, fields_json FROM templates')
        rows = c.fetchall()
        conn.close()

        templates = []
        for form_name, fields_json in rows:
            fields = json.loads(fields_json)
            templates.append({
                'form_name': form_name,
                'fields': fields
            })

        return jsonify({'templates': templates})

    except Exception as e:
        print(f"[ERROR] Failed to load templates: {e}")
        return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
