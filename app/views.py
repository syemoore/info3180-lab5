"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/
This file creates your application.
"""

from app import app, db
from flask import render_template, request, redirect, url_for, flash, jsonify, make_response
from models import UserProfile
from werkzeug.utils import secure_filename
import os
import datetime
import random
from forms import RegisterForm


###
# Routing for your application.
###

@app.route('/')
def home():
    """Render website's home page."""
    return render_template('home.html')


@app.route('/profile', methods=["GET", "POST"])
def profile():
    form = RegisterForm()
    
    if request.method == "POST":
        file_folder = app.config['UPLOADS']
        
        if form.validate_on_submit():
            
            fname = form.first_name.data
            lname = form.last_name.data
            age = form.age.data
            gender = form.gender.data
            biography = form.biography.data
            
            pic = request.files['image']
            image = secure_filename(pic.filename)
            pic.save(os.path.join(file_folder, image))
            
            userid = idGenerator(fname, lname, age)
            username = genUsername(fname)
            date_created = datetime.date.today()
            
            new = UserProfile(
                        uid=userid, 
                        username=username, 
                        firstname=fname, 
                        lastname=lname, 
                        biography=biography, 
                        image=image,
                        gender=gender,  
                        profile_created_on=date_created, 
                        age=age)
                
            db.session.add(new)
            db.session.commit()
            
            flash("Created Successfully", "success")
            return redirect(url_for("profile"))
            
    return render_template("profile.html", form=form)

@app.route('/profiles', methods=["GET", "POST"])
def profiles():
    
    users = UserProfile.query.all()
    user_list = [{"user": user.username, "userid": user.userid} for user in users]
    
    if request.method == "GET":
        file_folder = app.config['UPLOADS']
        return render_template("profiles.html", users=users)
    
    elif request.method == "POST":
        response = make_response(jsonify({"users": user_list}))                                           
        response.headers['Content-Type'] = 'application/json'            
        return response

@app.route('/profile/<userid>', methods=["GET", "POST"])
def userprofile(userid):
    
    user = UserProfile.query.filter_by(userid=userid).first()
    
    if request.method == "GET":
        file_folder = app.config['UPLOADS']
        return render_template("view_user.html", user=user)
    
    elif request.method == "POST":
        if user is not None:
            response = make_response(jsonify(userid=user.userid, username=user.username, image=user.image, gender=user.gender, age=user.age,
                    profile_created_on=user.profile_created_on))
            response.headers['Content-Type'] = 'application/json'            
            return response
        else:
            flash('No User Found', 'danger')
            return redirect(url_for("index"))

def idGenerator(fname, lname, age):
    nid = []
    for x in fname:
        nid.append(str(ord(x)))
    for x in lname:
        nid.append(str(ord(x)))
    nid.append(str(age))
    
    random.shuffle(nid)
    
    nid = "".join(nid)
    
    return nid[:7]
    
def genUsername(fname):
    return fname + str(random.randint(10,100))
    
if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0",port="8080")