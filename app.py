from flask import Flask
from flask import request, render_template
import json, os
from automation import Automate

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def home():
    x = Automate('163g1a0505').start()
    return x
    # if request.method == 'POST':
    #     rollno = request.form.get('rollno')
    #     rollno = rollno.upper()
    #     print(rollno)
    #     data = Automate(rollno).start()
    #     return render_template('res.html', data = data)
    # return render_template('base.html')


if __name__ == "__main__":
    app.run()
