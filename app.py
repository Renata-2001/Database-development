import os
import json
import uuid

import psycopg2 
from flask_login import LoginManager, login_user, login_required, current_user, logout_user
from flask import Flask, redirect, url_for, render_template, request, session, g, current_app, flash
from flask.cli import with_appcontext
from werkzeug.security import generate_password_hash, check_password_hash

from db import DanceDB
from login import UserLogin


app = Flask(__name__)


@app.route('/')
def index():
   return render_template('main.html')
  
dancedb = None
@app.before_request
def before_request():
 global dancedb
 dance_db = psycopg2.connect(dbname="dancedb", user="renatik", password = "Bizezo_00")
 dance_db = DanceDB(dance_db)

if __name__ == '__main__':
   app.run()