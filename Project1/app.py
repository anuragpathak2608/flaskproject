#Imported flask library for web development
from flask import Flask
from models import Base

#Imported db session form setupdb for intracting with db
from setupdb import db_session

#Imported tables(classes) models.py
from models import Users, Tasks

#Imported josniyf to send json in response
#Imported requests to fetch the body and from the http requests
from flask import jsonify, request

from datetime import datetime,timedelta
from flask import abort


#Create instance of flask
app = Flask(__name__)

#Create route
@app.route("/")
def hello():
    return "Hello World"


@app.route("/tasks")
def get_all_tasks():
    tasks = db_session.query(Tasks).all()
    task_list = []
    for task in tasks:
        if not task.tisdeleted:
            task_list.append(task.serialize())
    return jsonify(task_list)

@app.route("/tasks/deleted")
def get_all_deleted_tasks():
    all_del_task = db_session.query(Tasks).all()
    del_task_list = []
    if all_del_task is None:
        return {"msg": "no deleted task found1"}
    for task in all_del_task:
        print(task.tisdeleted)
        if task.tisdeleted == False:
            continue
        del_task_list.append(task.serialize())
        #else:
            #return {"msg": "no deleted task found"}
    return jsonify(del_task_list)


@app.route("/tasks", methods = ['POST'])
def create_new_task():
    #In post operation we first fetch the json received from client
    received_json = request.get_json()
    #Convert that Json into you object
    tasks_object = Tasks(received_json)
    db_session.add(tasks_object)
    db_session.commit()
    return {"id": tasks_object.tid, "msg": "task created"}


@app.route("/tasks/<id>")
def get_task_by_id(id):
    task_by_id = db_session.query(Tasks).get(id)
    if task_by_id is None:
        return {"msg": "Task not found"}
    return jsonify(task_by_id.serialize())


@app.route("/tasks/hard/<id>", methods=['DELETE'])
def hard_delete(id):
    delete_obj = db_session.query(Tasks).get(id)
    if delete_obj is None:
        return {"msg": "task not found"}

    if delete_obj.tisdeleted == True:
        db_session.delete(delete_obj)
        db_session.commit()
        return {"id": delete_obj.tid, "msg": "task deleted successfully"}
    else:
        return {"msg": "task can not be deleted first soft delete the task"}



@app.route("/tasks/<id>", methods=['DELETE'])
def soft_delete(id):
    task_to_delete =  db_session.query(Tasks).get(id)
    if task_to_delete is None:
        return {"msg": "task not found"}
    if task_to_delete.tisdeleted is True:
        return {"msg": "task not found"}
    task_to_delete.tisdeleted = True
    db_session.commit()
    return {"id": task_to_delete.tid, "msg": "task deleted successfully"}



@app.route("/users", methods=['POST'])
def add_user():
    user_details = request.get_json()
    user_details_object = Users(user_details)
    db_session.add(user_details_object)
    db_session.commit()
    return {"id": user_details_object.uid, "msg": "user created successfully"}


@app.route("/users/<id>", methods=['DELETE'])
def del_user(id):
    delete_user = db_session.query(Users).get(id)
    if delete_user is None:
        return {"msg": "user not found"}
    db_session.delete(delete_user)
    db_session.commit()
    return {"id": id, "msg": "user deleted successfully"}


@app.route("/users/<id>")
def get_user_by_id(id):
    user_object = db_session.query(Users).get(id)
    if user_object is None:
        return {"msg": "user not found"}
    return jsonify(user_object.serialize())


@app.route("/users")
def get_all_users():
    get_all_user_object = db_session.query(Users).all()
    if get_all_user_object == []:
        return {"msg": "no user found"}
    all_users_list = []
    for users in get_all_user_object:
        all_users_list.append(users.serialize())
    return jsonify(all_users_list)


if __name__ == "__main__":
    app.run(debug=True)
