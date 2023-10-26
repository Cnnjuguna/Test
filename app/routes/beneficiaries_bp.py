from app.extensions import db, ma, Resource, Api, Blueprint, request
from models.beneficiaries import Beneficiary

beneficiaries_bp = Blueprint("beneficiaries_bp", __name__)
api = Api(beneficiaries_bp)


# Schema for Beneficiary serialization
class BeneficiarySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Beneficiary


beneficiary_schema = BeneficiarySchema()
beneficiaries_schema = BeneficiarySchema(many=True)


# Beneficiary resource for getting a single beneficiary
class BeneficiaryResource(Resource):
    def get(self, beneficiary_id):
        beneficiary = Beneficiary.query.get(beneficiary_id)
        if not beneficiary:
            return {"message": "Beneficiary not found"}, 404
        result = beneficiary_schema.dump(beneficiary)
        return result

    # PUT operation to update a beneficiary
    def put(self, beneficiary_id):
        beneficiary = Beneficiary.query.get(beneficiary_id)
        if not beneficiary:
            return {"message": "Beneficiary not found"}, 404

        data = request.get_json()
        updated_beneficiary = beneficiary_schema.load(data, instance=beneficiary)
        db.session.commit()
        return beneficiary_schema.dump(updated_beneficiary)

    # DELETE operation to delete a beneficiary
    def delete(self, beneficiary_id):
        beneficiary = Beneficiary.query.get(beneficiary_id)
        if not beneficiary:
            return {"message": "Beneficiary not found"}, 404
        db.session.delete(beneficiary)
        db.session.commit()
        return {"message": "Beneficiary deleted"}, 204


# BeneficiaryList resource for creating new beneficiaries and viewing all beneficiaries
class BeneficiaryListResource(Resource):
    def get(self):
        beneficiaries = Beneficiary.query.all()
        result = beneficiaries_schema.dump(beneficiaries)
        return result

    def post(self):
        data = request.get_json()
        beneficiary = beneficiary_schema.load(data)
        db.session.add(beneficiary)
        db.session.commit()
        return beneficiary_schema.dump(beneficiary), 201


# Adding resources to the API
api.add_resource(BeneficiaryListResource, "/beneficiaries")
api.add_resource(BeneficiaryResource, "/beneficiaries/<int:beneficiary_id>")
