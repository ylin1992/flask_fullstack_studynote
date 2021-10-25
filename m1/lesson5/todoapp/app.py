from typing_extensions import final
from flask import Flask, request, url_for
from flask import json, abort
from flask.json import jsonify
from flask.templating import render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import exc
from werkzeug.utils import redirect
import sys
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://ewan@localhost:5432/todoapp'
db =  SQLAlchemy(app)


class Todo(db.Model):
    __tablename__ = 'todoapp'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(), nullable=False)

    def __repr__(self):
        return f'<Todo ID {self.id} description {self.description}>'


db.create_all()

@app.route('/')
def index():
    return render_template('index.html', data = Todo.query.all())

@app.route('/todos/create', methods=['POST'])
def create():
    #item = request.form.get('description', '') # the second parameter is the default value if nothing returns
    error = False
    body = {}
    try:
        item = request.get_json()['description']
        print(item)
        print(type(item))
        todo = Todo(description=item)
        db.session.add(todo)
        db.session.commit()
        body['description'] = todo.description
    except:
        error = True
        db.session.rollback()
        print(sys.exc_info())
    finally:
        # whether or not the commit has successfully completed
        # close the db
        db.session.close()
    
    # Note that by default, Flask erases all the instances if a commit is made
    # In the finally block, the db is closed, so the commit will always be made
    # and the "Todo" instance will be wiped out. 
    # To keep the information of newly built todo instance, we create a dictionary
    # storing the information
    if error:
        # abort the request with 400 status code
        abort(400)
    else:
        return jsonify(body)

if __name__ == '__main__':
    app.run(debug=True)