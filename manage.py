from flask import Flask,render_template,redirect
import os
from flask_sqlalchemy import SQLAlchemy 
import pymysql 
pymysql.install_as_MySQLdb()

app = Flask(__name__)

if __name__ == '__main__':
    app.run(debug=True,port=5656)
