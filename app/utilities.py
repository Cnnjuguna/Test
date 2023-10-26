import os
from .extensions import bcrypt


def verify_password(stored_password, provided_password):
    return bcrypt.check_password_hash(stored_password, provided_password)


# utilities.py

import os


def write_secret_key_to_env(secret_key):
    env_file = ".env"

    if not os.path.exists(env_file):
        # If the .env file doesn't exist, we create it
        with open(env_file, "w") as f:
            f.write(f"SECRET_KEY={secret_key}\n")
    else:
        # If the .env file already exists, check if SECRET_KEY is defined
        with open(env_file, "r") as f:
            lines = f.readlines()
            key_exists = False
            for i, line in enumerate(lines):
                if line.startswith("SECRET_KEY="):
                    # If SECRET_KEY is already defined, we update it
                    lines[i] = f"SECRET_KEY={secret_key}\n"
                    key_exists = True
                    break

            if not key_exists:
                # If SECRET_KEY is not defined, we then add it to the end of the file
                lines.append(f"SECRET_KEY={secret_key}\n")

        with open(env_file, "w") as f:
            f.writelines(lines)
