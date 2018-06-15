from flask import Flask, jsonify
app = Flask(__name__)

@app.route('/vacancies/simular/<int:id>')
def index(id):
    data = {'vacancies': [id]}
    return jsonify(data)