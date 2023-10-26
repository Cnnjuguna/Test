from ..extensions import db, ma, Resource, Api, Blueprint, request
from models.donations import Donation

donations_bp = Blueprint("donations_bp", __name__)
api = Api(donations_bp)


# Schema for Donation serialization
class DonationSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Donation


donation_schema = DonationSchema()
donations_schema = DonationSchema(many=True)


# Donation resource for getting a single donation
class DonationResource(Resource):
    def get(self, donation_id):
        donation = Donation.query.get(donation_id)
        if not donation:
            return {"message": "Donation not found"}, 404
        result = donation_schema.dump(donation)
        return result

    # PUT operation to update a donation
    def put(self, donation_id):
        donation = Donation.query.get(donation_id)
        if not donation:
            return {"message": "Donation not found"}, 404

        data = request.get_json()
        updated_donation = donation_schema.load(data, instance=donation)
        db.session.commit()
        return donation_schema.dump(updated_donation)

    # DELETE operation to delete a donation
    def delete(self, donation_id):
        donation = Donation.query.get(donation_id)
        if not donation:
            return {"message": "Donation not found"}, 404
        db.session.delete(donation)
        db.session.commit()
        return {"message": "Donation deleted"}, 204


# DonationList resource for creating new donations and viewing all donations
class DonationListResource(Resource):
    def get(self):
        donations = Donation.query.all()
        result = donations_schema.dump(donations)
        return result

    def post(self):
        data = request.get_json()

        # We check if the donation is recurring
        is_recurring = data.get("recurring", False)

        if is_recurring:
            # Handling recurring donation creation
            donation = self.create_recurring_donation(data)
        else:
            # Handling one-time donation creation
            donation = donation_schema.load(data)

        db.session.add(donation)
        db.session.commit()
        return donation_schema.dump(donation), 201

    def create_recurring_donation(self, data):
        # Creates a new recurring Donation record
        donation = donation_schema.load(data)
        db.session.add(donation)
        db.session.commit()

        # Handling scheduling for recurring donations (explained below)
        self.schedule_recurring_donation_processing(donation)

        return donation

    def schedule_recurring_donation_processing(self, donation):
        if donation.recurring:
            # Scheduling the recurring donation processing task using Celery (explained earlier)
            update_next_donation_dates.apply_async(
                args=[donation.donation_id], eta=donation.next_donation_date
            )


# Adding resources to the API
api.add_resource(DonationListResource, "/donations")
api.add_resource(DonationResource, "/donations/<int:donation_id>")
