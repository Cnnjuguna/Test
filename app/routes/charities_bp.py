# charities_bp.py
from flask import Blueprint, request, jsonify, Schema, fields, Api, ma
from app import db
import flask_sqlalchemy
from ..models import Charity

charities_bp = Blueprint("charities", __name__)
api = Api(charities_bp)


class CharitySchema(ma.Schema):
    class Meta:
        model = Charity


# Charity Resource for getting a single charity
class CharityResource(ma.SQLAlchemyAutoSchema):
    def get(self, charity_id):
        charity = Charity.query.get(charity_id)
        if not charity:
            return {"message": "Charity not found"}, 404
        result = CharitySchema().dump(charity)
        return result

    def put(self, charity_id):
        charity = Charity.query.get(charity_id)
        if not charity:
            return {"message": "Charity not found"}, 404

        data = request.get_json()
        charity_schema = CharitySchema()
        updated_charity = charity_schema.load(data, instance=charity)
        db.session.commit()
        return charity_schema.dump(updated_charity)

    def delete(self, charity_id):
        charity = Charity.query.get(charity_id)
        if not charity:
            return {"message": "Charity not found"}, 404
        db.session.delete(charity)
        db.session.commit()
        return {"message": "Charity deleted"}, 204


class CharityListResource(Resour)