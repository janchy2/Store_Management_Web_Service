from flask_sqlalchemy import SQLAlchemy

database = SQLAlchemy()

class User(database.Model):
    __tablename__ = "users"

    id = database.Column(database.Integer, primary_key=True, autoincrement=True)
    email = database.Column(database.String(256), nullable=False)
    password = database.Column(database.String(256), nullable=False)
    forename = database.Column(database.String(256), nullable=False)
    surname = database.Column(database.String(256), nullable=False)
    role = database.Column(database.String(256), nullable=False)
