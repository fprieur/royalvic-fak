"""Main module for the royal vic first aid kit website."""


import os
import datetime
from flask import Flask, render_template
#from flask_peewee.db import Database
#from flask_peewee.auth import Auth
#from flask_peewee.admin import Admin, ModelAdmin
#from peewee import *
from flask.ext.admin import Admin
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.admin.contrib.sqla import ModelView

SECRET_KEY = 'ssshhhh'

app = Flask(__name__)
#app.config['DEBUG'] = True
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost/firstaidkit'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://zfwhcfwipnfyrx:pvE27NW2AEGAech-motmk8RXXD@ec2-23-21-170-57.compute-1.amazonaws.com:5432/d8t86dcvos3s5m'
#app.config['SQLALCHEMY_ECHO'] = True
# instantiate the db wrapper
db = SQLAlchemy(app)

# create an Auth object for use with our flask app and database wrapper
#auth = Auth(app, db)
#admin = Admin(app, auth, branding="Admin - RoyalVic First Aid Kit")
admin = Admin(app, name="Admin - RoyalVic First Aid Kit")

class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    lastname = db.Column(db.String(80))
    firstname = db.Column(db.String(80))
    title = db.Column(db.String(80))

    def __unicode__(self):
        return self.title + ' ' + self.firstname + ' ' + self.lastname


admin.add_view(ModelView(Person, db.session))

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


admin.add_view(ModelView(Section, db.session))
#class SectionAdmin(ModelAdmin):
#    columns = ('title', 'description')

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    name = db.Column(db.String(80))
    person_id = db.Column(db.Integer, db.ForeignKey('person.id'))
    person = db.relationship('Person', backref=db.backref('projects', lazy='dynamic'))
    section_id = db.Column(db.Integer, db.ForeignKey('section.id'))
    section = db.relationship('Section', backref=db.backref('section', lazy='dynamic'))
    description = db.Column(db.Text)
    amountGoal = db.Column(db.Integer)
    amountFunded = db.Column(db.Integer)
    thumbnail = db.Column(db.String(255))

    def __unicode__(self):
        return self.title

#   def __unicode__(self):
#        return '%s: ' % (self.section)

admin.add_view(ModelView(Project, db.session))

#db.create_all()

@app.route("/")
def home():
    """home return the home page."""
    return render_template("index.html")


@app.route("/projects")
def projects():
    """projects return projects page."""
    projects = []
    for p in Project.query.all():
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
    id = 0
    for s in Section.query.all():
        if s.title.lower() == section:
            id = s.id
    result = Project.query.filter_by(section_id = id).all()
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
