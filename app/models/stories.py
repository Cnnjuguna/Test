from ..extensions import db, migrate


class Story(db.Model):
    __tablename__ = "stories"
    id = db.Column(db.Integer, primary_key=True)
    charity_id = db.Column(
        db.Integer, db.ForeignKey("charities.charity_id"), nullable=False
    )
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text)
    status = db.Column(db.String(20), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(
        db.DateTime,
        default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp(),
    )

    # Relationship
    charity = db.relationship("Charity", backref="stories")
