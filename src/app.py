# Import libraries
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

# Setting connection to db with sqlalchemy
app = Flask(__name__)

# Connection to our Data Base
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root@localhost/flaskmysql'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

db = SQLAlchemy(app)
ma = Marshmallow(app)

# Making the table with ORM
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(70), unique=True)
    description = db.Column(db.String(100))

    def __init__(self, title, description):
        self.title = title
        self.description = description

db.create_all() # Makes the table

# Schema to interact
class TaskSchema(ma.Schema):
    class Meta:
        fields = ('id', 'title', 'description')

# We will interact with these variables
task_schema = TaskSchema()
tasks_schema = TaskSchema(many=True)

# Routes to interact or end points
@app.route('/tasks', methods=['POST'])
def create_task():

    # Variables to save our json content
    title = request.json['title']
    description = request.json['description']

    # Making new task
    new_task = Task(title, description)

    # Saving into our db
    db.session.add(new_task)
    db.session.commit()

    # Returning the new task to the client to see new changes
    return task_schema.jsonify(new_task)

@app.route('/tasks', methods=['GET'])
def get_tasks():

    # Getting the new task 
    all_tasks = Task.query.all()
    result = tasks_schema.dump(all_tasks)
    return jsonify(result)

@app.route('/tasks/<id>', methods=['GET'])
def get_task(id):

    # We will show just the required task by id
    task = Task.query.get(id)
    return task_schema.jsonify(task)

@app.route('/tasks/<id>', methods=['PUT'])
def update_task(id):
    task = Task.query.get(id)

    title = request.json['title']
    description = request.json['description']

    task.title = title
    task.description = description

    # Update to our db
    db.session.commit()
    return task_schema.jsonify(task)

@app.route('/tasks/<id>', methods=['DELETE'])
def delete_task(id):

    # Delete process 
    task = Task.query.get(id)
    db.session.delete(task)
    db.session.commit()

    return task_schema.jsonify(task)

@app.route('/', methods=['GET'])
def index():
    return jsonify({'message': 'Welcome to this API'})


if __name__ == "__main__":
    app.run(debug=True)






