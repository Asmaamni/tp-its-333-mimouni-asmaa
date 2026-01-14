from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required # type: ignore
import sqlite3

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = "super-secret-key"
jwt = JWTManager(app)

DB_FILE = "database.db"

# on initialise la base de données
def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS person (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

init_db()

# Route pour récupérer un token
@app.route("/login", methods=["POST"])
def login():
    token = create_access_token(identity="user")
    return jsonify(access_token=token)

# CRUD personnes
@app.route("/persons", methods=["POST"])
@jwt_required()
def create_person():
    data = request.json
    name = data.get("name")
    if not name:
        return jsonify(error="Name is required"), 400

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO person (name) VALUES (?)", (name,))
    person_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return jsonify(id=person_id, name=name), 201

@app.route("/persons/<int:person_id>", methods=["GET"])
@jwt_required()
def get_person(person_id):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT id, name FROM person WHERE id = ?", (person_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return jsonify(id=row[0], name=row[1])
    return jsonify(error="Person not found"), 404

@app.route("/persons/<int:person_id>", methods=["DELETE"])
@jwt_required()
def delete_person(person_id):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM person WHERE id = ?", (person_id,))
    conn.commit()
    conn.close()
    return jsonify(message="Person deleted")

# Démarrage du serveur Flask
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)