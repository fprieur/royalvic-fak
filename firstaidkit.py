"""Main module for the royal vic first aid kit website."""


import os
from flask import Flask, render_template

app = Flask(__name__)

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
