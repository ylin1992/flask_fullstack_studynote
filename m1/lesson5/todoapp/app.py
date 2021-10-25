from flask import Flask
from flask.templating import render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', data = [
        {'description' : 'TODO1'},
        {'description' : 'TODO2'},
        {'description' : 'TODO3'}
    ])


if __name__ == '__main__':
    app.run(debug=True)