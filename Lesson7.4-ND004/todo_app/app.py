from flask import Flask, request, render_template, jsonify, abort, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import sys

# named after name of file
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://student:password@localhost:5432/todoapp'
db = SQLAlchemy(app)

migrate = Migrate(app,db)

class Todo(db.Model):
    __tablename__ = 'todos'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(), nullable=False)
    completed = db.Column(db.Boolean, nullable=False, default=False)
    def __repr__(self):
        return f'<Todo {self.id} {self.description}>'

# comment this out for flask db init
# db.create_all()

@app.route('/todos/<todo_id>', methods=['DELETE'])
def set_delete_todo(todo_id):
    try:
        Todo.query.filter_by(id=todo_id).delete()
        db.session.commit()
    except:
        db.session.rollback()
    finally:
        db.session.close()
    return jsonify({ 'success': True })

@app.route('/todos/<todo_id>/set-completed', methods=['POST'])
def set_completed_todo(todo_id):
    try:
        completed = request.get_json()['completed']
        todo = Todo.query.get(todo_id)
        todo.completed = completed
        db.session.commit()
    except:
        db.session.rollback()
    finally:
        db.session.close()

    # redirect to /index 
    return redirect(url_for('index'))

@app.route('/todos/create', methods=['POST'])
def create_todo():

    # implement try-except-finally for our db.session create task
    # variables for db session
    error = False
    body = {}

    try:
        description = request.get_json()['description']
        todo = Todo(description=description)
        db.session.add(todo)
        db.session.commit()
        body['description'] = todo.description
    except:
        error = True
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()

    if error:
        abort (500)
    else:
        return jsonify(body )


# route that listens to homepage
@app.route('/')
def index():
    return render_template('index.html', data=Todo.query.order_by('id').all())


if __name__ == '__main__':
# requires app.secret_key setting if updating database
    app.secret_key = 'SUPER SECRET'
    # set to False when in "Run and Debug" mode in vscode
    app.debug=True
    app.run(host='0.0.0.0',port=5000,threaded=False)
