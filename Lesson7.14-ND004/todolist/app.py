from flask import Flask, request, render_template, jsonify, redirect, abort, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import sys

# named after name of file
app = Flask(__name__)
app.config[
    'SQLALCHEMY_DATABASE_URI'] = 'postgresql://student:password@localhost:5432/todoapp'
db = SQLAlchemy(app)

migrate = Migrate(app, db)


class Todo(db.Model):
    __tablename__ = 'todos'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(), nullable=False)
    completed = db.Column(db.Boolean, nullable=False, default=False)
    # establish foreign key with parent table 'TodoList'
    list_id = db.Column(db.Integer,
                        db.ForeignKey('todolists.id'),
                        nullable=False)

    def __repr__(self):
        return f'<Todo {self.id} {self.description} {self.completed} {self.list_id}>'


class TodoList(db.Model):
    __tablename__ = 'todolists'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    # establish db.relationship with child table 'Todo'
    todos = db.relationship('Todo', backref='list', lazy=True)

    def __repr__(self):
        return f'<TodoList {self.id} {self.name}>'


@app.route('/lists/create', methods=['POST'])
def create_todoList():

    error = False
    body = {}

    try:
        name = request.get_json()['name']
        todoList = TodoList(name=name)
        db.session.add(todoList)
        db.session.commit()
        body['id'] = todoList.id
        body['name'] = todoList.name
    except:
        error = True
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()

    if error:
        abort(500)
    else:
        return jsonify(body)


@app.route('/todos/create', methods=['POST'])
def create_todo():

    # implement try-except-finally for our db.session create task
    # variables for db session
    error = False
    body = {}

    try:
        description = request.get_json()['description']
        list_id = request.get_json()['list_id']
        todo = Todo(description=description, completed=False, list_id=list_id)
        todo.list = list
        db.session.add(list)
        db.session.commit()
        body['description'] = todo.description
        body['list_id'] = active_list.id
    except:
        error = True
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()

    if error:
        abort(500)
    else:
        return jsonify(body)


@app.route('/todos/<todo_id>', methods=['DELETE'])
def set_delete_todo(todo_id):
    try:
        Todo.query.filter_by(id=todo_id).delete()
        db.session.commit()
    except:
        db.session.rollback()
    finally:
        db.session.close()
    return jsonify({'success': True})
    # return redirect(url_for('index'))


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


# new route to display lists depending on the list_id
@app.route('/lists/<list_id>')
def get_list_todos(list_id):
    return render_template(
        'index.html',
        lists=TodoList.query.all(),
        active_list=TodoList.query.get(list_id),
        todos=Todo.query.filter_by(list_id=list_id).order_by('id').all())


# route that listens to homepage
@app.route('/')
# @app.route('/todos')
def index():
    return redirect(url_for('get_list_todos', list_id=1))


if __name__ == '__main__':
    # requires app.secret_key setting if updating database
    app.secret_key = 'SUPER SECRET'
    # set to False when in "Run and Debug" mode in vscode
    app.debug = True
    app.run(host='0.0.0.0', port=5000, threaded=False)
