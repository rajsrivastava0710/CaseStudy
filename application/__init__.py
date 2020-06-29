from flask import Flask
from config import Config
from flask_mysqldb import MySQL


app = Flask(__name__)

app.config.from_object(Config)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'ashutosh@1998'
app.config['MYSQL_DB'] = 'hospitalknit'

mysql = MySQL(app)

from application import route