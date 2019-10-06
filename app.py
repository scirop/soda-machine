from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import sys

#initialize app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///soda_machines.db'
db = SQLAlchemy(app)

from views import *
