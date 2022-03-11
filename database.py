# imports

from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from sqlalchemy import Column, Integer, ForeignKey, String, Text
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from main import db


class Users(UserMixin, db.Model):
    __tablename__ = "users",
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
    priority = Column(String(250), nullable=False)
    date = Column(String(250), nullable=False)
    img = Column(String, nullable=True)

    # relationship with Users table
    submitter_id = Column(Integer, ForeignKey("users.id"))
    submitter = relationship("Users", back_populates="bugs")


class Comment(db.Model):
    __tablename__ = "comments"
    id = Column(Integer, primary_key=True)
    text = Column(Text, nullable=False)

    # relationship with Users table
    commenter_id = Column(Integer, ForeignKey("users.id"))
    commenter = relationship("Users", back_populates="comments")


