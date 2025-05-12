import os
from flask import Flask, jsonify
import sqlite3
import json

app = Flask(__name__)

DB_PATH = os.path.join(os.path.dirname(__file__), 'templates.db')

@app.route('/templates', methods=['GET'])
def get_templates():
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

if __name__ == '__main__':
    app.run(debug=True)