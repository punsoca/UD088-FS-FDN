from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://student:password@localhost:5432/todoapp'
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String, nullable=False)

    def __repr__(self):
        return f'<Todo {self.id} {self.description}'

db.create_all()


@app.route('/')
def index():
    return  render_template('index.html', data=[{
            'description': 'To Do 1'
        }, {
            'description': 'To Do 2'

        }, {
            'description': 'To Do 3'

        }])


if __name__ == '__main__':
    app.debug=True
    app.run(host='0.0.0.0',port=5000,threaded=False)
