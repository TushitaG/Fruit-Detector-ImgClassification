from fileinput import filename
from pyparsing import Char
from application import app, db, photos
from application.models import User,Entry
from application.forms import LoginForm
from datetime import datetime
from flask import render_template, request, flash, json, jsonify, redirect, render_template, session, url_for
from flask_login import login_required, logout_user, current_user, login_user
from flask_cors import CORS, cross_origin
from keras.preprocessing import image
from keras.preprocessing.image import load_img
from PIL import Image, ImageOps
import re
import base64
from io import BytesIO
import numpy as np
import requests
from cv2 import *
import uuid
import json
from json import JSONEncoder
#Global list for look up
fruits_type = ['Fresh Apple', 'Fresh Banana', 'Fresh Lemon', 'Fresh Lulo', 'Fresh Mango','Fresh Orange', 'Fresh Strawberry', 'Fresh Tamarillo', 'Fresh Tomato','Rotten Apple', 'Rotten Banana', 'Rotten Lemon', 'Rotten Lulo', 'Rotten Mango','Rotten Orange', 'Rotten Strawberry', 'Rotten Tamarillo', 'Rotten Tomato']
logged_in = False

def add_entry(new_entry):
    try:
        db.session.add(new_entry)
        db.session.commit()
        return new_entry.id

    except Exception as error:
        db.session.rollback()
        flash(error,"danger")

def parseImage(imgData):
    imgstr = re.search(b'base64,(.*)', imgData).group(1)
    with open('output.png','wb') as output:
        output.write(base64.decodebytes(imgstr))
    im = Image.open('output.png').convert('RGB')
    #im_invert = ImageOps.invert(im)
    im.save('output.png')

    # global char
    # global userid
    # char = uuid.uuid1()
    # imgstr = re.search(b'base64,(.*)', imgData).group(1)
    # with open(f'application/images/{char}.png','wb') as output:
    #     output.write(base64.decodebytes(imgstr))
    # im = Image.open(f'application/images/{char}.png')
    # # im_invert = ImageOps.invert(im.convert('grayscale'))
    # im.save(f'application/images/{char}.png')


def make_prediction(instances):
    data = json.dumps({"signature_name": "serving_default", "instances": instances.tolist()})
    headers = {"content-type": "application/json"}
    json_response = requests.post(url, data=data, headers=headers)
    predictions = json.loads(json_response.text)['predictions']
    return predictions

def add_entry(new_entry):
    try:
        db.session.add(new_entry)
        db.session.commit()
        return new_entry.id
 
    except Exception as error:
        db.session.rollback()
        flash(error,"danger")

def get_entries():
    try:
        entries = Entry.query.all()
        return entries
    except Exception as error:
        db.session.rollback()
        flash(error,"danger") 
        return 0

def remove_entry(id):
    try:
        entry = Entry.query.get(id)
        db.session.delete(entry)
        db.session.commit()
    except Exception as error:
        db.session.rollback()
        flash(error,"danger")
 
#server URL
url = 'https://ca2-2b02-jumanatushita-tf.herokuapp.com/v1/models/img_classifier:predict'


#create the database if not exist
db.create_all()

#Handles http://127.0.0.1:5000/
@app.route('/')
@app.route('/index') 
@app.route('/home') 
def index_page(): 
    if logged_in == False:
        return render_template("index.html",index=True, logged_in=False)
    elif logged_in == True:
        return render_template("index.html", index=True, logged_in=True)
@app.route('/predict', methods=['GET','POST']) 
@cross_origin(origin='localhost',headers=['Content- Type','Authorization'])
def predict_page(): 
    # global file
    
    # file = 'ee6d8193-8af5-11ec-b9ea-84c5a6c1f33f.png'
    if logged_in == False:
        form = LoginForm()
        return render_template("login.html", index=True, form=form, logged_in=False)
    elif logged_in == True:
        if request.method == 'POST':
            # print(request.get_data())
            parseImage(request.get_data())
            img = image.img_to_array(image.load_img("output.png", color_mode="rgb", target_size=(224, 224))) / 255.
            # img = image.img_to_array(image.load_img(f'application/images/ee6d8193-8af5-11ec-b9ea-84c5a6c1f33f.png.png', color_mode='rgb', target_size=(224,224))) /255.
            img = img.reshape(1, 224, 224,3)
            # new_entry = Entry(userid=userid, filename=f'{char}.png', prediction='rotten',predicted_on=datetime.utcnow())
            # add_entry(new_entry)
            # # Decoding and pre-processing base64 image
            # img = image.img_to_array(image.load_img("output.png", color_mode="grayscale", target_size=(28, 28))) / 255.
            # # reshape data to have a single channel
            # img = img.reshape(1,28,28,1)
        
            predictions = make_prediction(img)
        
            ret = ""
            for i, pred in enumerate(predictions):
                ret = "{}".format(np.argmax(pred))
                response = ret

                return response
                
            
        return render_template("predict.html", index=True, logged_in=True)


@app.route('/history') 
def history_page(): 
    if logged_in == False:
        form = LoginForm()
        return render_template("login.html", index=True, form=form, logged_in=False)
    elif logged_in == True:
        return render_template("history.html", index=True, logged_in=True, entries=get_entries())


@app.route("/login", methods=["GET", "POST"]) 
def login_page(): 
    global logged_in 
    global userid 
    form = LoginForm() 
    if request.method == 'POST': 
        if form.validate_on_submit(): 
            email = form.email.data 
            password = form.password.data 
            user = User.query.filter(User.email==email).first() 
            if user == None: 
                logged_in = False 
                flash("User not found.") 
            else: 
                user = User.query.filter(User.email == email, User.password==password).first() 
                if user == None: 
                    logged_in = False 
                    flash("Wrong Email or Wrong Password!") 
                else: 
                    userid=user.id  
                    logged_in = True 
                    return render_template('index.html', form=form, logged_in=True, userid=userid) 
        else: 
            logged_in = False 
            flash(f"Login Error") 
    logged_in = False 
    return render_template("login.html", form=form, logged_in=False)


@app.route("/logout")
def logout():
    logged_in==False
    return render_template("index.html", index=True, logged_in=False)

# @app.route('/remove', methods=['POST'])
# def remove():
#     form = PredictionForm()
#     req = request.form
#     id = req["id"]
#     remove_entry(id)
#     return render_template("history.html", 
#         title="Remove History Records", 
#         form=form, entries = get_entries(), index=True )
@app.route('/remove', methods=['POST'])
def remove():
    id = userid
    remove_entry(id)
    return render_template("history.html", 
        title="Remove History Records", entries = get_entries(), index=True)

#API: add entry
@app.route("/api/add", methods=['POST'])
def api_add(): 
    #retrieve the json file posted from client
    data = request.get_json()
    #retrieve each field from the data
    filename      = data['filename']
    prediction     = data['prediction']
    #create an Entry object store all data for db action
    new_entry = Entry(  houseSize=filename,prediction=prediction,predicted_on=datetime.utcnow())
    #invoke the add entry function to add entry                        
    result = add_entry(new_entry)
    #return the result of the db action
    return jsonify({'id':result})

def get_entry(id):
    try:
        entries = Entry.query.filter(Entry.id==id)
        result = entries[0]
        return result
    except Exception as error:
        db.session.rollback()
        flash(error,"danger") 
        return 0

    
#API get entry
@app.route("/api/get/<id>", methods=['GET'])
def api_get(id): 
    #retrieve the entry using id from client
    entry = get_entry(int(id))
    print(entry)
    #Prepare a dictionary for json conversion
    data = {'id'             : entry.id,
            'filename'      : entry.filename,
            'prediction'     : entry.prediction}
    #Convert the data to json
    result = jsonify(data)
    return result #response back


#API delete entry
@app.route("/api/delete/<id>", methods=['GET'])
def api_delete(id): 
    entry = remove_entry(int(id))
    return jsonify({'result':'ok'})


#API get all entries
@app.route("/api/getall", methods=['GET'])
def api_getAll(): 
    entries = get_entries()
    data=[]
    for entry in entries:
        d = {'id'           : entry.id,
            'filename'      : entry.filename,
            'prediction'    : entry.prediction}
        data.append(d)
    result = jsonify(data)
    return result