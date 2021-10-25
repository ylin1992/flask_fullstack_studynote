from flask import Flask, request, url_for
from flask.templating import render_template
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import redirect
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
    item = request.form.get('description', '') # the second parameter is the default value if nothing returns
    print(item)
    print(type(item))
    db.session.add(Todo(description=item))
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)