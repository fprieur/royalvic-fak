"""Main module for the royal vic first aid kit website."""


import os
import datetime
from flask import Flask, render_template
from flask.ext.admin import Admin
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.admin.contrib.sqla import ModelView
from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand


app = Flask(__name__)
app.config['DEBUG'] = True

app.secret_key = os.urandom(24)

#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost/firstaidkit'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://zfwhcfwipnfyrx:pvE27NW2AEGAech-motmk8RXXD@ec2-23-21-170-57.compute-1.amazonaws.com:5432/d8t86dcvos3s5m'
#app.config['SQLALCHEMY_ECHO'] = True
# instantiate the db wrapper
db = SQLAlchemy(app)
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

admin = Admin(app, name="Admin - RoyalVic First Aid Kit")

class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    lastname = db.Column(db.String(80))
    firstname = db.Column(db.String(80))
    title = db.Column(db.String(80))

    def __unicode__(self):
        return self.title + ' ' + self.firstname + ' ' + self.lastname


admin.add_view(ModelView(Person, db.session))

class About(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    howDoesItWorkTitle = db.Column(db.String(80))
    howDoesItWorkContent = db.Column(db.String(120))
    ourMissionTitle = db.Column(db.String(80))
    ourMissionContent = db.Column(db.String(120))
    otherQuestionTitle = db.Column(db.String(80))
    otherQuestionContent = db.Column(db.String(120))

#admin.add_view(ModelView(About, db.session))

class Section(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    description = db.Column(db.String(120))

    def __unicode__(self):
        return self.title


admin.add_view(ModelView(Section, db.session))


class AboutPage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bigTitle = db.Column(db.String(80))
    hditwTitle = db.Column(db.String(80))
    hdiwContent = db.Column(db.Text)
    missionTitle = db.Column(db.String(80))
    missionContent = db.Column(db.Text)
    QuestionTitle = db.Column(db.String(80))
    QuestionContent = db.Column(db.Text)

    def __unicode__(self):
        return self.bigTitle


admin.add_view(ModelView(AboutPage, db.session))

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
    akaraisin_url = db.Column(db.String(255))

    def __unicode__(self):
        return self.title

#   def __unicode__(self):
#        return '%s: ' % (self.section)

admin.add_view(ModelView(Project, db.session))

db.create_all()
manager.run()
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
            "akaraisin_url": p.akaraisin_url,
        })
    return render_template("projects.html", projects=projects)

@app.route("/projectsv1")
def projectsv1():
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
            "akaraisin_url": p.akaraisin_url,
        })
    return render_template("projectsv1.html", projects=projects)

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
            "akaraisin_url": p.akaraisin_url,
        })
    return render_template("projectsBySection.html", projects=projects)


@app.route("/about")
def about():
    """about return the about page."""
    about = []
    result = AboutPage.query.all()
    for a in result:
        about.append({
            "bigTitle": a.bigTitle,
            "hditwTitle": a.hditwTitle,
            "hdiwContent": a.hdiwContent,
            "missionTitle": a.missionTitle,
            "missionContent": a.missionContent,
            "QuestionTitle": a.QuestionTitle,
            "QuestionContent": a.QuestionContent,
        })
    return render_template("about.html", about=about)

@app.route("/donate")
def donate():
    """donate return the donate form."""
    return render_template("donate.html")

@app.errorhandler(404)
def page_not_found(e):
        return render_template('404.html'), 404
