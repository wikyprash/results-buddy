from flask import Flask
from flask import request, render_template
import json, os
from automation import Automate

app = Flask(__name__)

def checkData(rollno):
    # if os.path.isfile(f'src\\results\\{rollno}.json'):
    #     with open(f'src\\results\\{rollno}.json', 'r') as f:
    #         obj = json.load(f)
    #         if rollno == obj['user']['Hall Ticket No']:
    #             data = obj
    #             return data
    # else:
        x = Automate(rollno)
        data = x.start()
        return data

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        rollno = request.form.get('rollno')
        rollno = rollno.upper()
        print(rollno)
        data = Automate(rollno).start()
        return render_template('res.html', data = data)
    return render_template('base.html')


if __name__ == "__main__":
    app.run()
