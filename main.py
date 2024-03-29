# imports

from flask import Flask, render_template, redirect, url_for, flash, request, session
from flask_bootstrap import Bootstrap
from flask_ckeditor import CKEditor
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, ForeignKey, String, Text
from sqlalchemy.ext.declarative import declarative_base
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from forms import AddBugForm, RegisterForm, LoginForm, CommentForm, StatusForm,\
    ProjectAssignForm, ProjectUnassignedForm, RoleAssign, EditUser
from graphs import CreatePriorityBar, CreatePie, CreateTimeBar
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
Base = declarative_base()

# Connect to Database

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///bugtracker.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

# Create database tables

# Association table for many to many relationship between Users and Bugs table
UsersBugs = db.Table(
    "usersbugs",
    db.Column("user_id", Integer, ForeignKey("users.id")),
    db.Column("bug_id", Integer, ForeignKey("bugs.id"))
)


class Users(UserMixin, db.Model):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    full_name = Column(String(100), nullable=False)
    email = Column(String(250), nullable=False, unique=True)
    password = Column(String(250), nullable=False)
    role = Column(String(250), nullable=True)

    # relationship with Bugs table
    bugs = relationship("Bugs", secondary=UsersBugs, backref=db.backref("assigned", lazy="dynamic"))

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
    date_added = Column(String, nullable=False)
    date_updated = Column(String, nullable=False)
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
    return Users.query.get(int(user_id))


# admin only function
def admin_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.role == "Admin":
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
        check_password = form.confirm_password.data
        user_email = form.email.data
        if Users.query.filter_by(email=user_email).first():

            # Flash message saying duplicated email
            flash("That email already exists, try login instead.")
            return redirect(url_for("login"))
        elif user_password != check_password:
            flash("The passwords do not match, try again.")
            return redirect(url_for("register"))
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

            # assign admin role to first account registered
            if user.id == 1:
                user.role = "Admin"
                db.session.commit()

            return redirect(url_for("dashboard"))

    return render_template("register.html", form=form)


@app.route("/dashboard", methods=["GET", "POST"])
@login_required
def dashboard():
    projects = Bugs.query.all()
    proj_count = len(projects)
    return render_template("dashboard.html", proj_count=proj_count)


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
            status="Not Started",
            date_added=datetime.now().strftime("%H:%M:%S %d/%m/%Y"),
            date_updated=datetime.now().strftime("%H:%M:%S %d/%m/%Y")
        )

        db.session.add(new_bug)
        db.session.commit()

        current_user.bugs.append(new_bug)
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
    projects = Bugs.query.all()
    return render_template("personal_projects.html", projects=projects)


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
        time_to_fix=project.time_to_fix,
    )

    if form.validate_on_submit():
        project.bug_name = form.bug_name.data
        project.brief_desc = form.brief_desc.data
        project.full_desc = form.full_desc.data
        project.priority = form.priority.data
        project.time_to_fix = form.time_to_fix.data
        project.date_updated = datetime.now().strftime("%H:%M:%S %d/%m/%Y")
        db.session.commit()
        return redirect(url_for("view_projects", project_id=project.id))

    return render_template("add_project.html", form=form, delete=True, project=project)


@app.route("/view_projects/<int:project_id>", methods=["GET", "POST"])
@login_required
def view_projects(project_id):
    project = Bugs.query.get(project_id)
    user_list = Users.query.all()
    form = CommentForm()
    status_form = StatusForm()
    assign_form = ProjectAssignForm()
    assign_form.users.choices = [(user.full_name, f"{user.full_name} - {user.role.title()}") for user in user_list]
    unassign_form = ProjectUnassignedForm()
    unassign_form.users.choices = [(user.full_name, f"{user.full_name} - {user.role.title()}") for user in project.assigned]
    if len(unassign_form.users.choices) == 1:
        unassign_ability = False
    else:
        unassign_ability = True


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
        project_to_update.date_updated = datetime.now().strftime("%H:%M:%S %d/%m/%Y")
        db.session.commit()
        return redirect(url_for("view_projects", project_id=project_id))

    return render_template("full_project_view.html", project=project, form=form, status=status_form, assign=assign_form, unassign=unassign_form, unassign_ability=unassign_ability)


@app.route("/assign_user/<int:project_id>", methods=["GET", "POST"])
def assign_user(project_id):
    if request.method == "POST":
        project = Bugs.query.get(project_id)
        user = request.form.get("users")
        assigned_user = Users.query.filter_by(full_name=user).first()
        project.assigned.append(assigned_user)
        db.session.commit()
        return redirect(url_for("view_projects", project_id=project_id))


@app.route("/unassign_user/<int:project_id>", methods=["GET", "POST"])
def unassign_user(project_id):

    if request.method == "POST":
        project = Bugs.query.get(project_id)
        user = request.form.get("users")
        full_user = Users.query.filter_by(full_name=user).first()

        project.assigned.remove(full_user)
        db.session.commit()

        return redirect(url_for("view_projects", project_id=project_id))


@app.route("/delete_project/<int:project_id>", methods=["GET", "POST"])
@login_required
@admin_only
def delete_project(project_id):
    project_to_delete = Bugs.query.get(project_id)
    db.session.delete(project_to_delete)
    db.session.commit()
    return redirect(url_for("all_projects"))


@app.route("/manage_users", methods=["GET", "POST"])
@login_required
def all_users():
    users = Users.query.all()
    form = RoleAssign()

    roles = ["Admin", "Team Leader", "Manager", "Senior Developer", "Developer", "Graduate Developer", "Junior Developer", "Part-Time Developer"]

    form.users.choices = [(user.full_name, user.full_name) for user in users]

    form.role.choices = roles
    if request.method == "POST" and form.users.data:
        for user in form.users.data:
            user_to_assign = Users.query.filter_by(full_name=user).first()
            user_to_assign.role = form.role.data
            db.session.commit()
        return redirect(url_for("all_users"))
    return render_template("users.html", users=users, form=form)


@app.route("/edit_profile/<int:user_id>", methods=["GET", "POST"])
@login_required
def edit_profile(user_id):
    user = Users.query.get(user_id)
    form = EditUser(
        name=user.full_name,
        email=user.email
    )
    if request.method == "POST":
        name = form.name.data
        email = form.email.data
        password = form.password.data
        confirm_password = form.confirm_password.data
        if password != confirm_password:
            flash("Passwords do not match, try again.")
            return redirect(url_for("edit_profile", user_id=user_id))
        else:
            user.password = password
            user.full_name = name
            user.email = email
            user.password = generate_password_hash(password, method="pbkdf2:sha256", salt_length=8)
            db.session.commit()
            return redirect(url_for("dashboard"))

    return render_template("user_profile.html", user=user, form=form)


@app.route("/dashboard/pie_chart")
@login_required
def pie_chart():
    projects = Bugs.query.all()
    CreatePie(data=projects)
    return render_template("pie_chart.html")


@app.route("/dashboard/priority_chart")
@login_required
def priority_chart():
    projects = Bugs.query.all()
    CreatePriorityBar(projects)
    return render_template("priority_chart.html")


@app.route("/dashboard/time_chart")
@login_required
def time_chart():
    projects = Bugs.query.all()
    CreateTimeBar(projects)
    return render_template("time_chart.html")


if __name__ == "__main__":
    app.run(debug=True)
