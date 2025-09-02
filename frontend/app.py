from flask import Flask, render_template
import os
import requests

app = Flask(__name__)

PORT = int(os.environ.get("PORT", "9000"))

BACKEND_URL = os.environ.get("BACKEND_URL", "http://localhost:8000")


@app.route('/')
def home():
    response=requests.get(f"{BACKEND_URL}/api/get")
    data=response.json()
    env=dict(os.environ)
    return render_template('index.html', env=env,data=data['data'])

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=PORT)
