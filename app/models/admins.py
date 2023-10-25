from ..extensions import db, migrate


class Admin(db.Model):
    __tablename__ = "admins"
    admin_id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey("user.id"), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(
        db.DateTime,
        default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp(),
    )

    user = db.relationship("User", backref="admin")
    charities = db.relationship("Charity", backref="admin")
