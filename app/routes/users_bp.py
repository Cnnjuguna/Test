from ..extensions import db, Blueprint, request, Resource, Api
from ..models.users import User

users_bp = Blueprint("users_bp", __name__)
api = Api(users_bp)


class DonorRegistration(Resource)

@users_bp.route("/users")
def get_users():
    users = [user for user in User.query.all()]
