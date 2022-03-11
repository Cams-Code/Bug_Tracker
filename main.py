# imports
import sqlalchemy as sqlalchemy
from flask import Flask, render_template, redirect, url_for, flash, request
from flask_bootstrap import Bootstrap
from flask_ckeditor import CKEditor
from datetime import date
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, ForeignKey, String, Text
from sqlalchemy.ext.declarative import declarative_base
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from forms import AddBugForm, RegisterForm, LoginForm, CommentForm
from flask_gravatar import Gravatar
from functools import wraps
from flask import abort
# from database import Users, Bugs
import os

# Initialising app

app = Flask(__name__)
app.config['SECRET_KEY'] = "super_secret_key"
Bootstrap(app)

# Initialising addons

login_manager = LoginManager()
login_manager.init_app(app)
ckeditor = CKEditor(app)

# Connect to Database

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///bugtracker.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

# Connect to tables


# user_loader callback
@login_manager.user_loader
def load_user(user_id):
    return


# View pages


@app.route("/", methods=["GET", "POST"])
def login():
    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        pass
    return render_template("register.html", form=form)


if __name__ == "__main__":
    app.run(debug=True)
