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

# Create database tables


class Users(UserMixin, db.Model):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    full_name = Column(String(100), nullable=False)
    email = Column(String(250), nullable=False, unique=True)
    password = Column(String(250), nullable=False)
    role = Column(String(250), nullable=True)

    # relationship with Bugs table
    bugs = relationship("Bugs", back_populates="submitter")

    # relationship with Comment table
    comments = relationship("Comment", back_populates="commenter")


class Bugs(db.Model):
    __tablename__ = "bugs"
    id = Column(Integer, primary_key=True)
    bug_name = Column(String(250), nullable=False)
    brief_desc = Column(String(250), nullable=False)
    full_desc = Column(Text(1000), nullable=False)
    time = Column(Integer, nullable=True)
    severity = Column(Integer, nullable=True)
    priority = Column(Integer, nullable=False)
    date = Column(String(250), nullable=False)
    img = Column(String, nullable=True)

    # relationship with Users table
    submitter_id = Column(Integer, ForeignKey("users.id"))
    submitter = relationship("Users", back_populates="bugs")

    # relationship with Comment table
    comments = relationship("Comment", back_populates="bug")


class Comment(db.Model):
    __tablename__ = "comments"
    id = Column(Integer, primary_key=True)
    text = Column(Text, nullable=False)

    # relationship with Users table
    commenter_id = Column(Integer, ForeignKey("users.id"))
    commenter = relationship("Users", back_populates="comments")

    # relationship with Bugs table
    bug_id = Column(Integer, ForeignKey("bugs.id"))
    bug = relationship("Bugs", back_populates="comments")


# Create tables in db
db.create_all()


# user_loader callback
@login_manager.user_loader
def load_user(user_id):
    return


# View pages


@app.route("/", methods=["GET", "POST"])
def login():
    form = LoginForm()
    return render_template("login.html", form=form)


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        pass
    return render_template("register.html", form=form)


if __name__ == "__main__":
    app.run(debug=True)
