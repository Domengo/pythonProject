
"""
This module contains Flask routes for calculating pi and translating text.
"""

from flask import Flask, request
import math
import requests
from flask_cors import CORS
from getpass import getpass
import os
from dotenv import load_dotenv
load_dotenv()


app = Flask(__name__)
CORS(app)

if "BEARER_TOKEN" in os.environ:
    BEARER_TOKEN = os.environ["BEARER_TOKEN"]
else:
    BEARER_TOKEN = getpass("Enter you Cloudflare API Token(BEARER_TOKEN)")

if "ACCOUNT_ID" in os.environ:
    ACCOUNT_ID = os.environ["ACCOUNT_ID"]
else:
    ACCOUNT_ID = getpass("Enter your account id")
    
print(ACCOUNT_ID, BEARER_TOKEN)

API_BASE_URL = "https://api.cloudflare.com/client/v4/accounts//ai/run/"
headers = {"Authorization": "Bearer ", "Access-Control-Allow-Origin": "*"}

def run(model, inputs):
    response = requests.post(f"{API_BASE_URL}{model}", headers=headers, json=inputs)
    return response.json()


@app.route('/pi')
def calculate_pi():
    pi = math.pi
    return f"The value of pi is: {pi}"

@app.route('/translate', methods=['POST'])
def translate_text():
    model = '@cf/meta/m2m100-1.2b'
    inputText = {
        "text": request.form.get('text'),
        "source_lang": request.form.get('source_lang'),
        "target_lang": request.form.get('target_lang')
    }
    output = run(model, inputText)
    return output
if __name__ == '__main__':
    app.run()
