import secrets
import string


def generate_licence_key(prefix: str) -> str:
    chars = string.ascii_uppercase + string.digits

    def get_chunk(length: int = 4):
        return ''.join(secrets.choice(chars) for _ in range(length))

    return f"{prefix}-{get_chunk()}-{get_chunk()}-{get_chunk()}"
