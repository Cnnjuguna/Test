from app.routes.charity_applications_bp import charities_applications_schema
from ..extensions import db, ma, Blueprint, request, Resource, Api
from models.admins import Admin
from models.charities import Charity
from models.charity_applications import CharityApplications

admin_bp = Blueprint("admins", __name__)
api = Api(admin_bp)

# ...


# Resource for viewing pending charity applications
class PendingCharityApplicationsResource(Resource):
    def get(self):
        pending_applications = CharityApplications.query.filter_by(
            status="pending"
        ).all()
        result = charities_applications_schema(many=True).dump(pending_applications)
        return result


# Resource for approving or rejecting a charity application
class ApproveRejectCharityApplicationResource(Resource):
    def put(self, application_id):
        application = CharityApplications.query.get(application_id)
        if not application:
            return {"message": "Charity application not found"}, 404

        data = request.get_json()
        status = data.get("status")

        if status not in ("approved", "rejected"):
            return {"message": "Invalid status value"}, 400

        application.status = status
        db.session.commit()
        return {"message": "Charity application updated successfully"}


# Resource for deleting a charity
class DeleteCharityResource(Resource):
    def delete(self, charity_id):
        charity = Charity.query.get(charity_id)
        if not charity:
            return {"message": "Charity not found"}, 404

        db.session.delete(charity)
        db.session.commit()
        return {"message": "Charity deleted successfully"}


# Adding resources to the API
api.add_resource(PendingCharityApplicationsResource, "/admins/pending_applications")
api.add_resource(
    ApproveRejectCharityApplicationResource,
    "/admins/approve_reject_application/<int:application_id>",
)
api.add_resource(DeleteCharityResource, "/admins/delete_charity/<int:charity_id>")
