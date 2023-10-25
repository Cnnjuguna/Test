from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_blueprints import Blueprint
from flask_restful import Resource, Api
from marshmallow import Marshmallow, Schema, fields, validate


db = SQLAlchemy()
migrate = Migrate(app)
ma = Marshmallow()
