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
admin = Admin(app, auth, branding="Admin - RoyalVic First Aid Kit")


class Person(db.Model):
    lastname = CharField()
    firstname = CharField()
    title = CharField()

    def __unicode__(self):
        return self.title + ' ' + self.firstname + ' ' + self.lastname

class PersonAdmin(ModelAdmin):
    columns = ('lastname', 'firstname', 'title')

admin.register(Person, PersonAdmin)

class About(db.Model):
    bigTitleContent = CharField()
    howDoesItWorkTitle = CharField()
    howDoesItWorkContent = TextField()
    ourMissionTitle = CharField()
    ourMissionContent = TextField()
    otherQuestionTitle = CharField()
    otherQuestionContent = TextField()

admin.register(About)

class Section(db.Model):
    title = CharField()
    description = TextField()

    def __unicode__(self):
        return self.title


class SectionAdmin(ModelAdmin):
    columns = ('title', 'description')

admin.register(Section, SectionAdmin)

class Project(db.Model):
    title = CharField()
    name = CharField()
    person = ForeignKeyField(Person)
    section = ForeignKeyField(Section)
    description = TextField()
    amountGoal = CharField()
    amountFunded = CharField()
    thumbnail = CharField()

    def __unicode__(self):
        return '%s: ' % (self.section)

class ProjectAdmin(ModelAdmin):
    columns = ('title', 'section', 'amountGoal', 'amountFunded')

admin.register(Project, ProjectAdmin)

admin.setup()

# create tables
auth.User.create_table(fail_silently=True)
Person.create_table(fail_silently=True)
About.create_table(fail_silently=True)
Section.create_table(fail_silently=True)
Project.create_table(fail_silently=True)

@app.route("/")
def home():
    """home return the home page."""
    return render_template("index.html")


@app.route("/projects")
def projects():
    """projects return projects page."""
    projects = []
    for p in Project.select():
        # calculate percent funded to date
        #percentFundedToDate = 0
        #if int(p.amountFunded) > 0 and int(p.amountGoal) != 0:
        #    percentFundedToDate = (int(p.amountFunded) / int(p.amountGoal)) * 100
        projects.append({
            "title": p.title,
            "name": p.name,
            "description": p.description,
            "amountGoal": p.amountGoal,
            "amountFunded": p.amountFunded,
            "thumbnail": p.thumbnail,
        })
    return render_template("projects.html", projects=projects)


@app.route("/projects/<section>")
def projects_by_section(section):
    section_id = 0
    for s in Section.select():
        if s.title.lower() == section:
            section_id = s.id
    result = Project.select().where(Project.section == section_id)
    projects = []
    for p in result:
        projects.append({
            "title": p.title,
            "name": p.name,
            "description": p.description,
            "amountGoal": p.amountGoal,
            "amountFunded": p.amountFunded,
            "section": p.section,
            "thumbnail": p.thumbnail,
        })
    return render_template("projectsBySection.html", projects=projects)

@app.route("/about")
def about():
    """about return the about page."""
    return render_template("about.html")


@app.route("/donate")
def donate():
    """donate return the donate form."""
    return render_template("donate.html")
