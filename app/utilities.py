from .extensions import bcrypt


def verify_password(stored_password, provided_password):
    return bcrypt.check_password_hash(stored_password, provided_password)
