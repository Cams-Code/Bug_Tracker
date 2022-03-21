# imports

import sqlalchemy as sqlalchemy
from flask import Flask, render_template, redirect, url_for, flash, request, session
from flask_bootstrap import Bootstrap
from flask_ckeditor import CKEditor
from datetime import date
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, ForeignKey, String, Text
from sqlalchemy.ext.declarative import declarative_base
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from forms import AddBugForm, RegisterForm, LoginForm, CommentForm, StatusForm
from flask_gravatar import Gravatar
from functools import wraps
from flask import abort
from itsdangerous import URLSafeTimedSerializer
import os

# Initialising app

app = Flask(__name__)
app.config['SECRET_KEY'] = "super_secret_key"
Bootstrap(app)

# Initialising addons

login_manager = LoginManager()
login_manager.init_app(app)
ckeditor = CKEditor(app)
ts = URLSafeTimedSerializer(app.config["SECRET_KEY"])

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
    full_desc = Column(Text, nullable=False)
    time_to_fix = Column(Integer, nullable=False)
    priority = Column(Integer, nullable=False)
    status = Column(String(250), nullable=False)

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
# db.create_all()


# user_loader callback
@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))


# admin only function
def admin_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.role == "admin":
            return f(*args, **kwargs)
        else:
            return abort(403)

    return decorated_function


# View pages


@app.route("/", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if request.method == "POST":
        email = form.email.data
        password = form.password.data
        user = Users.query.filter_by(email=email).first()

        # check login credentials
        try:
            check_password_hash(user.password, password)
        except AttributeError:
            flash("That email does not exist, please try again.")
            return redirect(url_for("login"))
        else:
            if check_password_hash(user.password, password):
                login_user(user)
                session.permanent = False
                return redirect(url_for("dashboard"))
            else:
                flash("Incorrect password, please try again.")
                return redirect(url_for("login"))
    return render_template("login.html", form=form)


@app.route("/logout", methods=["GET", "POST"])
def logout():
    logout_user()
    return redirect(url_for("login"))


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        # Check for duplicated email
        user_name = form.name.data
        user_password = form.password.data
        user_email = form.email.data
        if Users.query.filter_by(email=user_email).first():

            # Flash message saying duplicated email
            flash("That email already exists, try login instead.")
            return redirect(url_for("login"))
        else:
            # add new user

            new_user = Users(
                full_name=user_name.title(),
                password=generate_password_hash(user_password, method="pbkdf2:sha256", salt_length=8),
                email=user_email,
                role="no role"
            )

            db.session.add(new_user)
            db.session.commit()

            # sign in when registered
            user = Users.query.filter_by(email=user_email).first()
            login_user(user)

            return redirect(url_for("dashboard"))

    return render_template("register.html", form=form)


@app.route("/dashboard", methods=["GET", "POST"])
@login_required
def dashboard():
    return render_template("dashboard.html")


@app.route("/add_bug", methods=["GET", "POST"])
@login_required
def add_bug():
    form = AddBugForm()
    if form.validate_on_submit():

        # add new bug to database
        new_bug = Bugs(
            bug_name=form.bug_name.data,
            brief_desc=form.brief_desc.data,
            full_desc=form.full_desc.data,
            time_to_fix=int(form.time_to_fix.data),
            priority=form.priority.data,
            submitter_id=current_user.id,
            status="Not Started"
        )

        db.session.add(new_bug)
        db.session.commit()

        return redirect(url_for("all_projects"))

    return render_template("add_project.html", form=form, delete=False)


@app.route("/all_projects", methods=["GET", "POST"])
@login_required
def all_projects():
    projects = Bugs.query.all()
    return render_template("all_projects.html", projects=projects)


@app.route("/personal_projects", methods=["GET", "POST"])
@login_required
def personal_projects():
    return render_template("personal_projects.html")


@app.route("/edit_projects/<int:project_id>", methods=["GET", "POST"])
@login_required
@admin_only
def edit_projects(project_id):
    project = Bugs.query.get(project_id)
    form = AddBugForm(
        bug_name=project.bug_name,
        brief_desc=project.brief_desc,
        full_desc=project.full_desc,
        priority=project.priority,
        time_to_fix=project.time_to_fix
    )

    if form.validate_on_submit():
        project.bug_name = form.bug_name.data
        project.brief_desc = form.brief_desc.data
        project.full_desc = form.full_desc.data
        project.priority = form.priority.data
        project.time_to_fix = form.time_to_fix.data
        db.session.commit()
        return redirect(url_for("view_projects", project_id=project.id))

    return render_template("add_project.html", form=form, delete=True, project=project)


@app.route("/view_projects/<int:project_id>", methods=["GET", "POST"])
@login_required
def view_projects(project_id):
    project = Bugs.query.get(project_id)
    form = CommentForm()
    status_form = StatusForm()

    # add comment
    if form.validate_on_submit() and form.comment.data:
        comment = form.comment.data
        new_comment = Comment(
            text=comment,
            commenter_id=current_user.id,
            bug_id=project.id,
        )

        db.session.add(new_comment)
        db.session.commit()
        return redirect(url_for("view_projects", project_id=project_id))

    # update status
    elif request.method == "POST" and status_form.status.data:
        new_status = status_form.status.data
        project_to_update = Bugs.query.get(project_id)
        project_to_update.status = new_status
        db.session.commit()
        return redirect(url_for("view_projects", project_id=project_id))

    return render_template("full_project_view.html", project=project, form=form, status=status_form)


@app.route("/delete_project/<int:project_id>", methods=["GET", "POST"])
@login_required
@admin_only
def delete_project(project_id):
    project_to_delete = Bugs.query.get(project_id)
    db.session.delete(project_to_delete)
    db.session.commit()
    return redirect(url_for("all_projects"))


@app.route("/all_users", methods=["GET", "POST"])
@login_required
def all_users():
    users = Users.query.all()
    return render_template("users.html", users=users)


@app.route("/manage_users", methods=["GET", "POST"])
@login_required
@admin_only
def manage_users():
    project = Bugs.query.get(1)
    return render_template("manage_users.html", project=project)


if __name__ == "__main__":
    app.run(debug=True)
