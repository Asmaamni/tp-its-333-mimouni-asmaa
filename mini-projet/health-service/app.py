from flask import Flask, request, jsonify
import json
import requests
from flask_jwt_extended import JWTManager, jwt_required # type: ignore

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = "super-secret-key"
jwt = JWTManager(app)

DATA_FILE = "data.json"
PERSON_SERVICE_URL = "http://person-service:5001/persons/"

# Fonctions pour lire et écrire le fichier JSON
def load_data():
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

# Vérifie que la personne existe via le service Person
def person_exists(person_id, token):
    headers = {"Authorization": f"Bearer {token}"}
    r = requests.get(PERSON_SERVICE_URL + str(person_id), headers=headers)
    return r.status_code == 200

# Routes CRUD
@app.route("/health/<int:person_id>", methods=["GET"])
@jwt_required()
def get_health(person_id):
    # Récupère le token JWT
    token = request.headers.get("Authorization", "").split(" ")[1]

    if not person_exists(person_id, token):
        return jsonify(error="Person not found"), 404

    data = load_data()
    return jsonify(data.get(str(person_id), {}))

@app.route("/health/<int:person_id>", methods=["POST", "PUT"])
@jwt_required()
def add_update_health(person_id):
    token = request.headers.get("Authorization", "").split(" ")[1]

    if not person_exists(person_id, token):
        return jsonify(error="Person not found"), 404

    data = load_data()
    data[str(person_id)] = request.json
    save_data(data)
    return jsonify(message="Health data saved")

@app.route("/health/<int:person_id>", methods=["DELETE"])
@jwt_required()
def delete_health(person_id):
    token = request.headers.get("Authorization", "").split(" ")[1]

    if not person_exists(person_id, token):
        return jsonify(error="Person not found"), 404

    data = load_data()
    data.pop(str(person_id), None)
    save_data(data)
    return jsonify(message="Health data deleted")

# Démarrage du serveur Flask
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002)
