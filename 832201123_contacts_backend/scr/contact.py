from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('contacts.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/contacts', methods=['GET'])
def get_contacts():
    conn = get_db_connection()
    contacts = conn.execute('SELECT * FROM contacts').fetchall()
    conn.close()
    return jsonify([dict(ix) for ix in contacts])

@app.route('/contacts', methods=['POST'])
def add_contact():
    new_contact = request.get_json()
    name = new_contact.get('name')
    phone = new_contact.get('phone')
    conn = get_db_connection()
    conn.execute('INSERT INTO contacts (name, phone) VALUES (?, ?)', (name, phone))
    conn.commit()
    conn.close()
    return jsonify({"status": "Contact added"}), 201

if __name__ == '__main__':
    app.run(debug=True)
