import os
from uuid import uuid4

from flask import Flask, request, render_template, send_from_directory,flash
import pandas as pd
import csv
from tensorflow.keras.models import load_model
import numpy as np
import string
import mysql.connector
import random, copy
import io
from PIL import Image
import re
import base64
import PIL
import cv2
from pylab import *
import math
import random




app = Flask(__name__)
app.config['SECRET_KEY'] = 'the random string'


classes = ['Classified food is cheese_plate:',
           'Classified food is cheesecake:','Classified food is chicken_curry:',
           'Classified food is chocolate_cake:','Classified food is cup_cakes:',
           'Classified food is donuts:','Classified food is dumplings:',
           'Classified food is french_fries:','Classified food is french_onion_soup:',
           'Classified food is fried_rice:','Classified food is frozen_yogurt:',
           'Classified food is garlic_bread:','Classified food is hamburger:',
           'Classified food is ice_cream:','Classified food is macarons:',
           'Classified food is omelette:','Classified food is onion_rings:',
           'Classified food is pancakes:',
           'Classified food is pizza:','Classified food is samosa:']

@app.route("/")
def index():
    return render_template("index.html")


@app.route('/registration')
def registration():
    return render_template("ureg.html",msg='Successfully Registered!!')

@app.route("/about")
def about():
    return render_template("about.html")

@app.route('/verify',methods = ["GET","POST"])
def verify():
    if request.method=='POST':
        name=request.form['name']
        email=request.form['email']
        pwd=request.form['pwd']
        cpass=request.form['cpass']
        pno=request.form['pno']
        print(pno)

        print("**************")

        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="",
            database="food_classification"
        )
        mycursor = mydb.cursor()

        print("**************")
        sql = "select * from ureg"
        result = pd.read_sql_query(sql, mydb)
        email1 = result['email'].values
        print(email1)
        if email in email1:
            flash("email already exists", "warning")
            return render_template('ureg.html')
        if (pwd == cpass):
            sql = "INSERT INTO ureg (name,email,pwd,pno) VALUES (%s,%s, %s,%s)"
            val = (name, email, pwd, pno)
            mycursor.execute(sql, val)
            mydb.commit()
            return render_template('user.html', msg="registered successfully")



@app.route('/userlog',methods=['POST', 'GET'])
def userlog():
    # global name, name1
    # global user
    if request.method == "POST":
        username = request.form['email']
        print(username)
        password1 = request.form['pwd']
        print(password1)
        print('p')
        mydb = mysql.connector.connect(host="localhost", user="root", password="", database="food_classification")
        cursor = mydb.cursor()
        sql = "select * from ureg where email='%s' and pwd='%s'" % (username, password1)
        print('q')
        x = cursor.execute(sql)
        print(x)
        results = cursor.fetchall()
        print(results)
        print(len(results))
        if len(results) > 0:
            print('r')
            flash("Welcome to website", "success")
            return render_template('userhome.html', msg=results[0][1])
        else:
            flash("Invalid Email/password", "danger")
            return render_template('user.html')

    return render_template('user.html')




@app.route('/userhome')
def userhome():
    return render_template("userhome.html",msg='Successfully logined!!')



@app.route('/upload1')
def upload1():
    return render_template("upload.html")


@app.route("/upload", methods=["POST","GET"])
def upload():
    if request.method=='POST':
        print('a')
        # m=int(request.form['alg'])

        myfile=request.files['file']
        fn=myfile.filename
        print("fghjkjdhk")
        mypath=os.path.join('D:/Fathima/Python/food class_1/images/', fn)
        print("gfdhgfagfajgf")
        myfile.save(mypath)

        print("aaaaaaaaaaaaaaaaa")

        print("{} is the file name",fn)
        print ("Accept incoming file:", fn)
        print ("Save it to:", mypath)
    #import tensorflow as tf
        import numpy as np
        from tensorflow.keras.preprocessing import image
        from tensorflow.keras.models import load_model
        new_model=load_model(r"D:\Fathima\Python\food class_1\resnet.h5")
        test_image=image.load_img(mypath, target_size=(128,128))


    # new_model.summary()
        # test_image = image.load_img('D:\\image classification\\images\\'+filename,target_size=(64,64))
        test_image = image.img_to_array(test_image)
        test_image = np.expand_dims(test_image, axis=0)
        result = new_model.predict(test_image)

        prediction=classes[np.argmax(result)]


        return render_template("template.html",image_name=fn, text=prediction)
    return render_template("upload.html")

print("bbbbbbbbbbbbbbbbbbbbbb")

@app.route('/upload/<filename>')
def send_image(filename):
    return send_from_directory("D:/Fathima/Python/food class_1/images", filename)
print("cccccccccccccccccccc")

@app.route('/view1/<filename>')
def view1(filename):

    return send_from_directory("D:/Fathima/Python/food class_1/images", filename)

if __name__ == "__main__":
    app.run(debug=True, threaded=False)


