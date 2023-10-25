from ..extensions import db, migrate


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True, nullable=False)
    email = db.Column(db.String(120), index=True, unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    role = db.Column(
        db.String(20), nullable=False
    )  # Roles: 'donor', 'recipient', 'admin'
    anonymous = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(
        db.DateTime,
        default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp(),
    )
    # Relationship
    admin = db.relationship("Admin", backref="user")

    def __repr__(self):
        return f"<User {self.username} | {self.role} >"
