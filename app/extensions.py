from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_blueprints import Blueprint
from flask_restful import Resource, Api
from marshmallow import Marshmallow, Schema, fields, validate
from flask import g, session, request, jsonify
from functools import wraps
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

login_manager = LoginManager()
bcrypt = Bcrypt()


db = SQLAlchemy()
migrate = Migrate()
ma = Marshmallow()
