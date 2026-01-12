from app import app

from flask import render_template, request, jsonify

### EXO1 - simple API

#@app.route('/')
#def index():
#    return "hello world"

### EXO2 - API with simple display

@app.route('/')
def index():
    return  render_template('index.html')

### EXO3 - API with parameters display 

### EXO4 - API with parameters retrieved from URL 
