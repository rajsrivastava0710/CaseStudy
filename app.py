from flask import Flask, render_template, flash, redirect, url_for, session, logging, request
#Basic Flask methods
from flask_mysqldb import MySQL 
# MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
# for form validation and input
from passlib.hash import sha256_crypt
#for password encryption
from functools import wraps
# for decorators

app = Flask(__name__)

# # MySQL COnfiguration
# app.config['MYSQL_HOST'] = 'localhost'
# app.config['MYSQL_USER'] = 'root'
# app.config['MYSQL_PASSWORD'] = 'raj'
# app.config['MYSQL_DB'] = 'blog_app'
# app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

#Initialize MySQL
mysql = MySQL(app)

#Index
@app.route('/')
def index():
    return render_template('home.html')

if __name__ == '__main__':
    app.secret_key = 'efew_5%&^8ndF4Q8zc]/'
    app.run(debug=True)