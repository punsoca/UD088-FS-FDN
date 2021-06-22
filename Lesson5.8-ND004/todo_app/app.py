from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
# named after name of file
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://student:password@localhost:5432/todoapp'
db = SQLAlchemy(app)


class Todo(db.Model):
    __tablename__ = 'todos'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(), nullable=False)
    def __repr__(self):
        return f'<Todo {self.id} {self.description}>'

db.create_all()

@app.route('/todos/create', methods=['POST'])
def create_todo():
    description = request.get_json()['description']
    # description = dict(request.form or request.json or request.data)[ "description"]
    todo = Todo(description=description)
    db.session.add(todo)
    db.session.commit()
    return jsonify({
        'description': todo.description
    })
    # return redirect(url_for('index', description=description))

# route that listens to homepage
@app.route('/')
def index():
    return render_template('index.html', data=Todo.query.all())


if __name__ == '__main__':
# requires app.secret_key setting if updating database
    app.secret_key = 'SUPER SECRET'
# set app.debug to False when in "Run and Debug" mode in vscode
    app.debug=True
    app.run(host='0.0.0.0',port=5000,threaded=False)
