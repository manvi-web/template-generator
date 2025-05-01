from flask import Flask, request, jsonify
import sqlite3
app = Flask(__name__)
def init_db():
    conn = sqlite3.connect('templates.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS templates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            form_name TEXT,
            fields TEXT
        )
    ''')
    conn.commit()
    conn.close()
@app.route('/save_template', methods=['POST'])
def save_template():
    data = request.get_json()
    form_name = data['form_name']
    fields = json.dumps(data['fields'])  # Save fields as string

    conn = sqlite3.connect('templates.db')
    c = conn.cursor()
    c.execute('INSERT INTO templates (form_name, fields) VALUES (?, ?)', (form_name, fields))
    conn.commit()
    conn.close()

    return jsonify({"message": "Template saved successfully!"})

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
