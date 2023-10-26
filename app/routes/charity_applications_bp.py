import flask_sqlalchemy
from ..extensions import Blueprint, request, Resource, Api, db, ma
from models import CharityApplications


charity_applications_bp = Blueprint("charity_applications", __name__)
api = Api(charity_applications_bp)


# Schema for CharityApplications serialization
class CharityApplicationsSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = CharityApplications


charity_application_schema = CharityApplicationsSchema()
charities_applications_schema = CharityApplicationsSchema(many=True)


# CharityApplication resource for getting a single application
class CharityApplicationResource(Resource):
    def get(self, application_id):
        application = CharityApplications.query.get(application_id)
        if not application:
            return {"message": "Application not found"}, 404
        result = charity_application_schema.dump(application)
        return result

    def put(self, application_id):
        application = CharityApplications.query.get(application_id)
        if not application:
            return {"message": "Application not found"}, 404

        data = request.get_json()
        updated_application = charity_application_schema.load(
            data, instance=application
        )
        db.session.commit()
        return charity_application_schema.dump(updated_application)

    def delete(self, application_id):
        application = CharityApplications.query.get(application)
        if not application:
            return {"message": "Application not found"}, 404

        db.session.delete(application)
        db.session.commit()
        return {"message": "Application deleted"}, 204


# CharityApplication resource for creating new applications
class CharityApplicationListResource(Resource):
    def get(self):
        applications = [application for application in CharityApplications.query.all()]
        result = charities_applications_schema.dump(applications)
        return result

    def post(self):
        data = request.get_json()
        application = charity_application_schema.load(data)
        db.session.add(application)
        db.session.commit()
        result = charity_application_schema.dump(application), 201
        return result


# Resources to the API
api.add_resource(CharityApplicationResource, "/charity_applications")
api.add_resource(
    CharityApplicationListResource, "/charity_applications/<int:application_id>"
)
