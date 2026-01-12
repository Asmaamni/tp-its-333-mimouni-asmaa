from flask import Flask, jsonify, request

app = Flask(__name__)

## EXO1: API GET: renvoyer un helloworld - API end point name: "api/salutation"

## EXO2: API POST: renvoyer un nom fourni en parametre - API end point name: "api/utilisateurs"

# to be tested with curl: 
# >> curl -i -X GET http://localhost:5000/api/salutation
# >> curl -i -X POST -H 'Content-Type: application/json' -d '{"nom": "Bob"}' http://localhost:5000/api/utilisateurs

if __name__ == '__main__':
    app.run(debug=True)