#Imported flask library for web development
from flask import Flask

#Imported db session form setupdb for intracting with db
from setupdb import db_session

#Imported tables(classes) models.py
from models import Users, Tasks

#Imported josniyf to send json in response
#Imported requests to fetch the body and from the http requests
from flask import jsonify, request

from datetime import datetime,timedelta




#Create instance of flask
app = Flask(__name__)

#Create route
@app.route("/")
def hello():
    return "Hello World"

@app.route("/tasks")
def get_all_tasks():
    tasks = db_session.query(Tasks).all()
    print("/n/n/n/n", tasks)
    task_list = []
    for task in tasks:
        task_list.append(task.serialize())
    return jsonify(task_list)


if __name__ == "__main__":
    app.run(debug=True)

