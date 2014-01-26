"""Main module for the royal vic first aid kit website."""


import os
from flask import Flask, render_template

app = Flask(__name__)

app.config.update(
    DEBUG = True,
)

@app.route("/")
def home():
    """home return the home page."""
    return render_template("index.html")


@app.route("/projects")
def projects():
    """projects return projects page."""
    return "Projects"


@app.route("/about")
def about():
    """about return the about page."""
    return "about page"
