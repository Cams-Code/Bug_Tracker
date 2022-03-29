# imports

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, TextField, SelectField, SelectMultipleField
from wtforms.validators import DataRequired, Email
from flask_ckeditor import CKEditorField


# WTForm linked to Bug database
class AddBugForm(FlaskForm):
    bug_name = StringField("Project Name", validators=[DataRequired()])
    brief_desc = StringField("Brief Description", validators=[DataRequired()])
    full_desc = CKEditorField("Full Description", validators=[DataRequired()])

    choices = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10)
    priority = SelectField("Priority (10 being very urgent)", choices=choices, validators=[DataRequired()])
    time_to_fix = SelectField("Estimated Time to fix (10 being very long)", choices=choices, validators=[DataRequired()])
    submit = SubmitField("Submit", render_kw={"class": "d-none d-sm-inline-block btn btn-sm btn-primary shadow-sm fas fa-sm text-white-50", "style": "width:100%;"})


# WTForm linked to User database
class RegisterForm(FlaskForm):
    name = StringField("", validators=[DataRequired()], render_kw={"placeholder": "Full Name", "class": "form-control"})
    email = StringField("", validators=[DataRequired(), Email()], render_kw={"placeholder": "Email Address", "class": "form-control"})
    password = PasswordField("", validators=[DataRequired()], render_kw={"placeholder": "Password", "class": "form-control"})
    confirm_password = PasswordField("", validators=[DataRequired()], render_kw={"placeholder": "Confirm Password", "class": "form-control"})
    submit = SubmitField("Register", render_kw={"class": "btn form-control btn-primary rounded submit px-3"})


# WTForm linked to User database
class LoginForm(FlaskForm):
    email = StringField("Email Address", validators=[DataRequired(), Email()], render_kw={"placeholder": "Email Address", "class": "form-control"})
    password = PasswordField("Password", validators=[DataRequired()], render_kw={"placeholder": "Password", "class": "form-control"})
    submit = SubmitField("Login", render_kw={"class": "btn form-control btn-primary rounded submit px-3"})


# WTForm linked to Comments database
class CommentForm(FlaskForm):
    comment = TextField("", validators=[DataRequired()], render_kw={"placeholder": "Add a new Comment", "class": "form-control"})
    submit = SubmitField("Submit", render_kw={"style": "transform: translate(0px, 4px)"})


# WTForm linked to changing Project status
class StatusForm(FlaskForm):
    choices = ("Not Started", "In Progress", "To Review", "Completed")
    status = SelectField("", choices=choices, validators=[DataRequired()])
    status_submit = SubmitField("Update", render_kw={"class": "btn btn-primary"})


# WTForm linked to assigning users to projects
class ProjectAssignForm(FlaskForm):
    users = SelectMultipleField(choices="", validators=[DataRequired()])
    assign_submit = SubmitField("Assign")


# WTForm linked to unassigning users to projects
class ProjectUnassignedForm(FlaskForm):
    users = SelectMultipleField(choices="", validators=[DataRequired()])
    unassign_submit = SubmitField("Unassign")


# WTForm linked to assigning users a role
class RoleAssign(FlaskForm):
    users = SelectMultipleField(choices="", validators=[DataRequired()], render_kw={"style": "font-weight: bold;"})
    role = SelectField(choices="", validators=[DataRequired()])
    role_submit = SubmitField("Submit")


# WTForm update user
class EditUser(FlaskForm):
    name = StringField("Full Name", validators=[DataRequired()])
    email = StringField("Email Address", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired()])
    submit = SubmitField("Register", render_kw={"class": "btn form-control btn-primary rounded submit px-3"})