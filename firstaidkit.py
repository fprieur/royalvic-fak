"""Main module for the royal vic first aid kit website."""


import os
import datetime
from flask import Flask, render_template
#from flask_peewee.db import Database
#from flask_peewee.auth import Auth
#from flask_peewee.admin import Admin, ModelAdmin
#from peewee import *
from flask.ext.sqlalchemy import SQLAlchemy

DEBUG = True
SECRET_KEY = 'ssshhhh'

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost/firstaidkit'

# instantiate the db wrapper
db = SQLAlchemy(app)

# create an Auth object for use with our flask app and database wrapper
#auth = Auth(app, db)
#admin = Admin(app, auth, branding="Admin - RoyalVic First Aid Kit")


class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    lastname = db.Column(db.String(80))
    firstname = db.Column(db.String(80))
    title = db.Column(db.String(80))

    def __init__(self, lastname, firstname, title):
        self.lastname = lastname
        self.firstname = firstname
        self.title = title

    def __unicode__(self):
        return self.title + ' ' + self.firstname + ' ' + self.lastname

#class PersonAdmin(ModelAdmin):
#    columns = ('lastname', 'firstname', 'title')

#admin.register(Person, PersonAdmin)

#class About(db.Model):
#    bigTitleContent = db.Column(db.String(80))
#    howDoesItWorkTitle = db.Column(db.String(80))
#    howDoesItWorkContent = db.Column(db.String(120))
#    ourMissionTitle = db.Column(db.String(80))
#    ourMissionContent = db.Column(db.String(120))
#    otherQuestionTitle = db.Column(db.String(80))
#    otherQuestionContent = db.Column(db.String(120))

#admin.register(About)

class Section(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    description = db.Column(db.String(120))

    def __unicode__(self):
        return self.title


#class SectionAdmin(ModelAdmin):
#    columns = ('title', 'description')

#admin.register(Section, SectionAdmin)

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    name = db.Column(db.String(80))
    #person_id = db.Column(db.Integer, db.ForeignKey('person.id'))
    #person = db.relationship('Person', backref=db.backref('projects', lazy='dynamic'))
    description = db.Column(db.String(120))
    amountGoal = db.Column(db.Integer)
    amountFunded = db.Column(db.Integer)
    thumbnail = db.Column(db.String(80))

    def __init__(self, title, name, description, amountGoal, amountFunded, thumbnail):
        self.title = title
        self.name = name
        #self.person = person
        self.description = description
        self.amountGoal = amountGoal
        self.amountFunded = amountFunded
        self.thumbnail = thumbnail

    def __unicode__(self):
        return self.title

#   def __unicode__(self):
#        return '%s: ' % (self.section)

#class ProjectAdmin(ModelAdmin):
#    columns = ('title', 'section', 'amountGoal', 'amountFunded')

#admin.register(Project, ProjectAdmin)

#admin.setup()

# create tables
#auth.User.create_table(fail_silently=True)
#Person.create_table(fail_silently=True)
#About.create_table(fail_silently=True)
#Section.create_table(fail_silently=True)
#Project.create_table(fail_silently=True)

db.create_all()
fred = Person('Prieur', 'Fred', 'mr')
project = Project('Marche avec postgres', 'postgres', 'allo', 300, 100, 'http://placehold.it/300x200')
db.session.add(fred)
db.session.add(project)
db.session.commit()

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

@app.errorhandler(404)
def page_not_found(e):
        return render_template('404.html'), 404
