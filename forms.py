# imports

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, URL, Email
from flask_ckeditor import CKEditorField


class AddBugForm(FlaskForm):
    pass


class RegisterForm(FlaskForm):
    name = StringField("Full Name", validators=[DataRequired()], render_kw={"placeholder": "Full Name", "class": "form-control"})
    email = StringField("Email Address", validators=[DataRequired(), Email()], render_kw={"placeholder": "Email Address", "class": "form-control"})
    password = PasswordField("Password", validators=[DataRequired()], render_kw={"placeholder": "Password", "class": "form-control"})
    submit = SubmitField("Register", render_kw={"class": "btn form-control btn-primary rounded submit px-3"})


class LoginForm(FlaskForm):
    email = StringField("Email Address", validators=[DataRequired(), Email()], render_kw={"placeholder": "Email Address", "class": "form-control"})
    password = PasswordField("Password", validators=[DataRequired()], render_kw={"placeholder": "Password", "class": "form-control"})
    submit = SubmitField("Login", render_kw={"class": "btn form-control btn-primary rounded submit px-3"})


class CommentForm(FlaskForm):
    comment = CKEditorField("Comment", validators=[DataRequired()])
    submit = SubmitField("Submit Comment")
