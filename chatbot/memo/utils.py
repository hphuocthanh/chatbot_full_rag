import hashlib
import secrets
import logging
import json


def generate_random_string(length=16):
    """
    Generates a random string of the specified length.
    """
    return secrets.token_hex(length // 2)  # Convert to bytes


def generate_request_id(max_length=32):
    """
    Generates a random string and hashes it using SHA-256.
    """
    random_string = generate_random_string()
    h = hashlib.sha256()
    h.update(random_string.encode('utf-8'))
    return h.hexdigest()[:max_length+1]


def extract_post_request(request):
    try:
        return json.loads(request.body.decode('utf-8'))
    except ValueError as err:
        logging.error(err)
        return {}

