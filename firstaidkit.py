"""Main module for the royal vic first aid kit website."""


import os
import datetime
from flask import Flask, render_template
from flask_peewee.db import Database
from flask_peewee.auth import Auth
from flask_peewee.admin import Admin, ModelAdmin
from peewee import *

# configure our database
DATABASE = {
        'name': 'firstaidkit.db',
        'engine': 'peewee.SqliteDatabase',
}
DEBUG = True
SECRET_KEY = 'ssshhhh'

app = Flask(__name__)

app.config.from_object(__name__)

# instantiate the db wrapper
db = Database(app)

# create an Auth object for use with our flask app and database wrapper
auth = Auth(app, db)

class Note(db.Model):
    message = TextField()
    created = DateTimeField(default=datetime.datetime.now)


class NoteAdmin(ModelAdmin):
    columns = ('message', 'created')

admin = Admin(app, auth)
admin.register(Note, NoteAdmin)

admin.setup()

# create tables
auth.User.create_table(fail_silently=True)
Note.create_table(fail_silently=True)

@app.route("/")
def home():
    """home return the home page."""
    return render_template("index.html")


@app.route("/projectsv1")
def projectsv1():
    """projects return projects page."""
    return render_template("projectsv1.html")


@app.route("/projectsv2")
def projectsv2():
    """projects return projects page."""
    return render_template("projectsv2.html")


@app.route("/about")
def about():
    """about return the about page."""
    return render_template("about.html")


@app.route("/donate")
def donate():
    """donate return the donate form."""
    return render_template("donate.html")
