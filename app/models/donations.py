from ..extensions import db, migrate


class Donation(db.Model):
    __tablename__ = "donations"
    id = db.Column(db.Integer, primary_key=True)
    donor_id = db.Column(db.Integer, db.ForeignKey("donors.donor_id"), nullable=False)
    charity_id = db.Column(
        db.Integer, db.ForeignKey("charities.charity_id"), nullable=False
    )
    amount = db.Column(db.Integer, nullable=False)
    admin_id = db.Column(db.Integer, db.ForeignKey("admins.admin_id"), nullable=False)
    donation_frequency = db.Column(db.String(20), nullable=False)
    total_donation_amount = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(
        db.DateTime,
        default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp(),
    )

    # Relationship
    donor = db.relationship("Donor", backref="donations")
    # Relationship
    charity = db.relationship("Charity", backref="donations")
