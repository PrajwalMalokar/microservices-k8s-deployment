from flask import Flask, render_template,jsonify
import os
from connections import coll

app = Flask(__name__)
PORT=os.environ.get("PORT",8000)

@app.route('/')
def home():

    return jsonify({"message": "Backend is Running"})

@app.route('/api/get')
def api():
    names = coll.find()
    result = []
    for name in names:
        result.append(name['value'])
    return jsonify({"data": result})

@app.route('/api/add/<name>')
def add_names(name):
    coll.insert_one({"value": name})
    return jsonify({"message": f"{name} added successfully"})

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port = PORT)
