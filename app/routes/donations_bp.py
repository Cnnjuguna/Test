from flask_blueprints import Blueprint
from ..extensions import db
from ..models.users import User

user_bp = Blueprint("user_bp", __name__)


@user_bp.route("/users")
def get_users():
    users = [user for user in User.query.all()]
