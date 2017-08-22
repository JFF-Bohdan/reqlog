import binascii
import hashlib

import ksuid

SALTING_ITERATIONS_COUNT = 100000


def create_hash(password, salt=None):
    if salt is None:
        salt = str(ksuid.ksuid())

    pw_bytes = password.encode("utf-8")
    salt_bytes = salt.encode("utf-8")

    dk = hashlib.pbkdf2_hmac("sha256", pw_bytes, salt_bytes, SALTING_ITERATIONS_COUNT)
    hashed_password = binascii.hexlify(dk).decode("ascii")

    return hashed_password, salt
