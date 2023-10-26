# charities_bp.py
from app.models.beneficiaries import Beneficiary
from app.routes.beneficiaries_bp import beneficiaries_schema
from ..extensions import (
    Blueprint,
    request,
    jsonify,
    Schema,
    fields,
    Api,
    ma,
    Schema,
    fields,
    validate,
    Resource,
    g,
    wraps,
)
from app import db
from ..models.charities import Charity
from ..models.beneficiaries import Beneficiary

charities_bp = Blueprint("charities", __name__)
api = Api(charities_bp)


class CharitySchema(ma.Schema):
    class Meta:
        model = Charity


charity_schema = CharitySchema()
charities_schema = CharitySchema(many=True)


# Authentication Decorator
def auth_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if not user_is_authenticated():
            return jsonify({"message": "Authentication required"}), 401
        return func(*args, **kwargs)

    return decorated_function


# Charity Resource for getting a single charity
class CharityResource(ma.SQLAlchemyAutoSchema):
    method_decorators = [auth_required]

    def get(self, charity_id):
        charity = Charity.query.get(charity_id)
        if not charity:
            return {"message": "Charity not found"}, 404
        result = charity_schema.dump(charity)
        return result

    def put(self, charity_id):
        charity = Charity.query.get(charity_id)
        if not charity:
            return {"message": "Charity not found"}, 404

        data = request.get_json()
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


# CharityList resource for creating new charities
class CharityListResource(Resource):
    def get(self):
        charities = Charity.query.all()
        result = charities_schema.dump(charities)
        return result

    def post(self):
        data = request.get_json()
        charity_schema = CharitySchema()
        charity = charity_schema.load(data)
        db.session.add(charity)
        db.session.commit()
        return charity_schema.dump(charity), 201


class BeneficiariesResources(Resource):
    method_decorators = [auth_required]

    def get(self):
        beneficiaries = Beneficiary.query.filter_by(charity_id=g.user.charity.id).all()
        result = beneficiaries_schema(many=True).dump(beneficiaries)
        return result


# Resource for a charity to maintain inventory sent to the beneficiaries
class InventoryResource(Resource):
    method_decorators = [auth_required]  # Requires authentication as a charity

    def post(self):
        data = request.get_json()
        # Process and store inventory data
        return {"message": "Inventory data saved successfully"}


# Add resources to the API
api.add_resource(CharityListResource, "/charities")
api.add_resource(CharityResource, "/charities/<int:charity_id>")
