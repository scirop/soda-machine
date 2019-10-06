from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import sys

#initialize app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///soda_machines.db'
db = SQLAlchemy(app)

if __name__ == "__main__":
    # We need to make sure Flask knows about its views before we run
    # the app, so we import them. We could do it earlier, but there's
    # a risk that we may run into circular dependencies, so we do it at the
    # last minute here.
    from views import *
    app.run()
