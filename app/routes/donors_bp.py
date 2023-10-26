from flask_blueprints import Blueprint
from ..extensions import db
from ..models.users import User

from app.extensions import db, ma, Resource, Api, Blueprint, request
from models.donors import Donor

donors_bp = Blueprint("donors_bp", __name__)
api = Api(donors_bp)


# Create a schema for Donor serialization
class DonorSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Donor


donor_schema = DonorSchema()
donors_schema = DonorSchema(many=True)


# Donor resource for getting a single donor
class DonorResource(Resource):
    def get(self, donor_id):
        donor = Donor.query.get(donor_id)
        if not donor:
            return {"message": "Donor not found"}, 404
        result = donor_schema.dump(donor)
        return result

    # PUT operation to update a donor
    def put(self, donor_id):
        donor = Donor.query.get(donor_id)
        if not donor:
            return {"message": "Donor not found"}, 404

        data = request.get_json()
        updated_donor = donor_schema.load(data, instance=donor)
        db.session.commit()
        return donor_schema.dump(updated_donor)

    # DELETE operation to delete a donor
    def delete(self, donor_id):
        donor = Donor.query.get(donor_id)
        if not donor:
            return {"message": "Donor not found"}, 404
        db.session.delete(donor)
        db.session.commit()
        return {"message": "Donor deleted"}, 204


# DonorList resource for creating new donors and viewing all donors
class DonorListResource(Resource):
    def get(self):
        donors = Donor.query.all()
        result = donors_schema.dump(donors)
        return result

    def post(self):
        data = request.get_json()
        donor = donor_schema.load(data)
        db.session.add(donor)
        db.session.commit()
        return donor_schema.dump(donor), 201


# Adding resources to the API
api.add_resource(DonorListResource, "/donors")
api.add_resource(DonorResource, "/donors/<int:donor_id>")
