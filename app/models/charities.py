from ..extensions import db, migrate


class Charity(db.Model):
    __tablename__ = "charities"
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text(250))
    admin_id = db.Column(db.Integer(), db.ForeignKey("admin.admin_id"), nullable=False)
    total_donation_amount = db.Column(db.Integer(), default=0)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(
        db.DateTime,
        default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp(),
    )

    # Relationships
    admin = db.relationship("Admin", backref="charity")
