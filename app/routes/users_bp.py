import flask_sqlalchemy
from ..extensions import db, Blueprint, request, Resource, Api, ma, bcrypt, session
from ..models.users import User
from ..utilities import verify_password

users_bp = Blueprint("users_bp", __name__)
api = Api(users_bp)


# Schema for serialization
class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User


user_schema = UserSchema()
users_schema = UserSchema(many=True)


# User resource for getting a single user
class UserResource(Resource):
    def get(self, user_id):
        user = User.query.get(user_id)

        if not user:
            return {"message": "User not found"}, 404
        result = user_schema.dump(user)
        return result

    def put(self, user_id):
        user = User.query.get(user_id)
        if not user:
            return {"message": "User not found"}, 404
        data = request.get_json()
        updated_user = user_schema.load(data, instance=user)
        db.session.commit()
        return user_schema.dump(updated_user)

    def delete(self, user_id):
        user = User.query.get(user_id)
        if not user:
            return {"message": "User not found"}, 404
        db.session.delete(user)
        db.session.commit()
        return {"message": "User deleted"}, 204


# UsersList resource for creating new users and viewing all users in the database
class UserListResource(Resource):
    def get(self):
        users = [user for user in User.query.all()]
        result = user_schema.dump(users)
        return result

    def post(self):
        data = request.get_json()
        password = data["password"]
        hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")
        user = User(
            username=data["username"],
            email=data["email"],
            password=hashed_password,
            role=data["role"],
        )
        db.session.add(user)
        db.session.commit()
        return user_schema.dump(user), 201


# User resource for login
class LoginResource(Resource):
    def post(self):
        data = request.get_json()
        user = User.query.filter_by(email=data["email"]).first()

        if user and verify_password(user.password, data["password"]):
            # User has logged successfully

            # Here we determine the role of the user and set it in the session
            session["user_id"] = user.id
            session["user_role"] = user.role

            return {"message": "User logged in successfully", "role": user.role}

        return {"message": "Invalid credentials"}, 401  # For Unauthorized access


# Logout resource
class LogoutResource(Resource):
    def post(self):
        if "user_id" in session:
            session.pop("user_id", None)
            session.pop("user_role", None)
        return {"message": "User logged out"}


api.add_resource(LoginResource, "/login")
api.add_resource(LogoutResource, "/logout")


# Resources to the API
api.add_resource(UserListResource, "/users")
api.add_resource(UserResource, "/users/<int:user_id>")
