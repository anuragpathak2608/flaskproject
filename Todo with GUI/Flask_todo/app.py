# Imported flask library for web development
from flask import Flask, render_template, redirect, url_for, flash
from models import Base

# Imported db session form setupdb for intracting with db
from setupdb import db_session

# Imported tables(classes) models.py
from models import Users, Tasks

# Imported josniyf to send json in response
# Imported requests to fetch the body and from the http requests
from flask import jsonify, request

from datetime import datetime, timedelta
from flask import abort

from flask_bootstrap import Bootstrap

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import Email, Length, InputRequired

# Create instance of flask
app = Flask(__name__)
Bootstrap(app)
app.config['SECRET_KEY'] = 'Secret'


class FormCreateUser(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=15)])
    email = StringField('Email', validators=[InputRequired(), Email(message='Invalid Email')])


class FormCreateTask(FlaskForm):
    title = StringField('title', validators=[InputRequired(), Length(min=4, max=30)])
    description = TextAreaField('description', validators=[InputRequired(), Length(max=500)])
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])


#Template to add user from from  GUI
@app.route('/user/add', methods=['GET', 'POST'])
def useradd():
    form = FormCreateUser()
    user_data = []
    if form.validate_on_submit():
        user_data.append(form.username.data)
        user_data.append(form.email.data)
        new_user = Users(user_data)
        db_session.add(new_user)
        db_session.commit()
        flash('You have been logged in!', 'success')
        return redirect(url_for('get_all_users'))
    else:
        flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('useradd.html', title='Add User', form=form)


#Template to add Task from from  GUI
@app.route('/task/add', methods=['GET', 'POST'])
def taskadd():
    form = FormCreateTask()
    data = []
    isdeleted = False
    isdone = False
    creationdate = datetime.now()
    print(creationdate)
    if form.validate_on_submit():
        data.append(form.username.data)
        data.append(form.title.data)
        data.append(form.description.data)
        data.append(isdeleted)
        data.append(isdone)
        data.append(creationdate)
        new_task = Tasks(data)
        db_session.add(new_task)
        db_session.commit()
        print(data)
        flash('You have been logged in!', 'success')
        return redirect(url_for('get_all_tasks'))
    else:
        flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('taskadd.html', title='Add Task', form=form)



@app.route("/register", methods=['GET', 'POST'])
def register():
    return "none"


@app.route("/api/test/<id>")
def api_test(id):
    task_by_id = db_session.query(Tasks).get(id)
    # if task_by_id is None:
    # return {"msg": "Task not found"}
    # print(task_by_id.serialize())
    data = task_by_id.serialize()
    print(data['id'])
    # return 'none'
    return render_template('home.html', data='data')


# API to list all the tasks which are not deleted(includes complete/incomplete)
@app.route("/api/tasks")
def api_get_all_tasks():
    tasks = db_session.query(Tasks).all()
    task_list = []
    for task in tasks:
        if not task.tisdeleted:
            task_list.append(task.serialize())
    return jsonify(task_list)


# Template to list all the tasks which are not deleted(includes complete/incomplete)
@app.route("/")
@app.route("/tasks")
def get_all_tasks():
    tasks = db_session.query(Tasks).all()
    task_list = []
    for task in tasks:
        # print(task.ttitle)
        if not task.tisdeleted:
            task_list.append(task.serialize())
    print(task_list[0])
    return render_template('home.html', task_list=task_list)


# API to list all the deleted tasks
@app.route("/api/tasks/deleted")
def api_get_all_deleted_tasks():
    all_del_task = db_session.query(Tasks).all()
    del_task_list = []
    if all_del_task is None:
        return {"msg": "no deleted task found1"}
    for task in all_del_task:
        print(task.tisdeleted)
        if task.tisdeleted == False:
            continue
        del_task_list.append(task.serialize())
    return jsonify(del_task_list)


# Template to list all the deleted tasks
@app.route("/tasks/deleted")
def get_all_deleted_tasks():
    all_del_task = db_session.query(Tasks).all()
    del_task_list = []
    if all_del_task is None:
        return '<h1>No deleted task found1</h1>'
    for task in all_del_task:
        print(task.tisdeleted)
        if task.tisdeleted == False:
            continue
        del_task_list.append(task.serialize())
    return render_template('deleted_task.html', del_task_list=del_task_list)


# API to create the task
@app.route("/api/tasks", methods=['POST'])
def api_create_new_task():
    # In post operation we first fetch the json received from client
    received_json = request.get_json()
    # Convert that Json into you object
    tasks_object = Tasks(received_json)
    tasks_object.tcreatedondate = datetime.now()
    db_session.add(tasks_object)
    db_session.commit()
    return {"id": tasks_object.tid, "msg": "task created"}, 201


# API to get the task by is ID
@app.route("/api/tasks/<id>")
def api_get_task_by_id(id):
    task_by_id = db_session.query(Tasks).get(id)
    if task_by_id is None:
        return {"msg": "Task not found"}
    return jsonify(task_by_id.serialize())


# API to hard delete(is deleted flag is True) the task
@app.route("/api/tasks/hard/<id>", methods=['DELETE'])
def api_hard_delete(id):
    delete_obj = db_session.query(Tasks).get(id)
    if delete_obj is None:
        return {"msg": "task not found"}

    if delete_obj.tisdeleted == True:
        db_session.delete(delete_obj)
        db_session.commit()
        return {"id": delete_obj.tid, "msg": "task deleted successfully"}
    else:
        return {"msg": "task can not be deleted first soft delete the task"}


# API to soft delete(sets isdeleted flag to True) the task
@app.route("/api/tasks/<id>", methods=['DELETE'])
def api_soft_delete(id):
    task_to_delete = db_session.query(Tasks).get(id)
    if task_to_delete is None:
        return {"msg": "task not found"}
    if task_to_delete.tisdeleted is True:
        return {"msg": "task not found"}
    task_to_delete.tisdeleted = True
    db_session.commit()
    return {"id": task_to_delete.tid, "msg": "task deleted successfully"}


# API to mark the task as completed.
@app.route("/api/tasks/<id>/done")
def api_task_as_done(id):
    task_obj = db_session.query(Tasks).get(id)
    if task_obj is None:
        return {"msg": "task not found"}

    if task_obj.tisdeleted is True:
        return {"msg": "You can not complete the tasks which are deleted"}

    task_obj.tisdone = True
    db_session.commit()
    return {"id": id, "msg": "task is completed"}


# API to show all completed task.
@app.route("/api/tasks/completed")
def api_get_all_completed_tasks():
    all_completed_tasks = db_session.query(Tasks).all()
    if all_completed_tasks is None:
        return {"msg": "no completed task found"}
    task_list = []
    for task in all_completed_tasks:
        if task.tisdone is True and task.tisdeleted is False:
            task_list.append(task.serialize())
    return jsonify(task_list)


# Template to show all completed task.
@app.route("/tasks/completed")
def get_all_completed_tasks():
    all_completed_tasks = db_session.query(Tasks).all()
    if all_completed_tasks is None:
        return '</h1>No completed task found</h1>'
    task_list = []
    for task in all_completed_tasks:
        if task.tisdone is True and task.tisdeleted is False:
            task_list.append(task.serialize())
    return render_template('completed_task.html', task_list=task_list)


# API to update the task.
# can be used to mark the task complete or delete the task
@app.route("/api/tasks/<id>", methods=['PUT'])
def api_upadate_task(id):
    task = Tasks.query.get(id)
    ttitle = request.json['ttitle']
    tdesc = request.json['tdesc']
    tcreatedbyuser = request.json['tcreatedbyuser']
    tisdeleted = request.json['tisdeleted']
    tisdone = request.json['tisdeleted']

    task.tisdeleted = tisdeleted
    task.ttitle = ttitle
    task.tdesc = tdesc
    task.tcreatedbyuser = tcreatedbyuser
    task.tisdone = tisdone

    db_session.commit()
    return {"id": id, "msg": "task updated successfully"}


# API to create the user.
@app.route("/api/users", methods=['POST'])
def api_add_user():
    user_details = request.get_json()
    user_details_object = Users(user_details)
    db_session.add(user_details_object)
    db_session.commit()
    return {"id": user_details_object.uid, "msg": "user created successfully"}, 201


# API to delete the perticluar user
@app.route("/api/users/<id>", methods=['DELETE'])
def api_del_user(id):
    delete_user = db_session.query(Users).get(id)
    if delete_user is None:
        return {"msg": "user not found"}
    db_session.delete(delete_user)
    db_session.commit()
    return {"id": id, "msg": "user deleted successfully"}


# API to get the details of the user by its ID.
@app.route("/api/users/<id>")
def api_get_user_by_id(id):
    user_object = db_session.query(Users).get(id)
    if user_object is None:
        return {"msg": "user not found"}
    return jsonify(user_object.serialize())


# API to list all the users
@app.route("/api/users")
def api_get_all_users():
    get_all_user_object = db_session.query(Users).all()
    if get_all_user_object == []:
        return {"msg": "no user found"}
    all_users_list = []
    for users in get_all_user_object:
        all_users_list.append(users.serialize())
    return jsonify(all_users_list)


# Template to list all the users
@app.route("/users")
def get_all_users():
    get_all_user_object = db_session.query(Users).all()
    if get_all_user_object == []:
        return '<h1>no user found</h1>'
    all_users_list = []
    for users in get_all_user_object:
        all_users_list.append(users.serialize())
    return render_template('users.html', title='Users', all_users_list=all_users_list)


if __name__ == "__main__":
    app.run(debug=True)
