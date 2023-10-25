from ..extensions import db, migrate


class CharityApplications(db.Model):
    __tablename__ = "charity_applications"
    id = db.Column(db.Integer(), primary_key=True)
    charity_id = db.Column(
        db.Integer(), db.ForeginKey("charities.charity_id"), nullable=False
    )
    admin_id = db.Column(db.Integer(), db.ForeignKey("admins.admin_id"), nullable=False)
    status = db.Column(db.String(20), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(
        db.DateTime,
        default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp(),
    )

    # Relationship
    charity = db.relationship("Charity", backref="applications")
