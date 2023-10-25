from ..extensions import db, migrate


class Beneficiary(db.Model):
    __tablename__ = "beneficiaries"
    id = db.Column(db.Integer, primary_key=True)
    charity_id = db.Column(
        db.Integer, db.ForeignKey("charities.charity_id"), nullable=False
    )
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(
        db.DateTime,
        default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp(),
    )

    # Relationship
    charity = db.relationship("Charity", backref="beneficiaries")
