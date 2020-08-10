from flask import Flask
from flask import request, render_template
from automation import Automate

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        rollno = request.form.get('rollno')
        rollno = rollno.upper()
        data = Automate(rollno).start()
        return render_template('res.html', data = data)
    return render_template('base.html')


if __name__ == "__main__":
    app.run()
