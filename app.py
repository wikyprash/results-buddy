from flask import Flask
from flask import request, render_template
from automation import Automate
import requests
import json

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        rollno = request.form.get('rollno')
        rollno = rollno.upper()
        data = requests.get("https://jntua-results-api.herokuapp.com/allAttemptedResults?htno=183g1a0501").text
        data = json.loads(data)
        return render_template('res.html', data = data)
    return render_template('base.html')


if __name__ == "__main__":
    app.run()
