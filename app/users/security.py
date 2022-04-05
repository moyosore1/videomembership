from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError


def generate_hash(password):
    ph = PasswordHasher()
    return ph.hash(password)


def verify_hash(hashed_password, raw_password):
    ph = PasswordHasher()
    verified = False
    message = ""

    try:
        verified = ph.verify(hashed_password, raw_password)
    except VerifyMismatchError:
        verified = False
        message = "Invalid password"
    except Exception as e:
        verified = False
        message = "An error occured"
    return verified, message
