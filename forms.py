# imports

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, URL, Email
from flask_ckeditor import CKEditorField


# WTForm linked to Bug database
class AddBugForm(FlaskForm):
    pass


# WTForm linked to User database
class RegisterForm(FlaskForm):
    name = StringField("", validators=[DataRequired()], render_kw={"placeholder": "Full Name", "class": "form-control"})
    email = StringField("", validators=[DataRequired(), Email()], render_kw={"placeholder": "Email Address", "class": "form-control"})
    password = PasswordField("", validators=[DataRequired()], render_kw={"placeholder": "Password", "class": "form-control"})
    submit = SubmitField("Register", render_kw={"class": "btn form-control btn-primary rounded submit px-3"})


# WTForm linked to User database
class LoginForm(FlaskForm):
    email = StringField("Email Address", validators=[DataRequired(), Email()], render_kw={"placeholder": "Email Address", "class": "form-control"})
    password = PasswordField("Password", validators=[DataRequired()], render_kw={"placeholder": "Password", "class": "form-control"})
    submit = SubmitField("Login", render_kw={"class": "btn form-control btn-primary rounded submit px-3"})


# WTForm linked to Comments database
class CommentForm(FlaskForm):
    comment = CKEditorField("Comment", validators=[DataRequired()])
    submit = SubmitField("Submit Comment")
