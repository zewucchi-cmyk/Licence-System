import secrets
import string

def generate_licence_key(prefix: str):
    chars = string.ascii_uppercase + string.digits

    def get_chunck(lenght: int = 4):
        return ''.join(secrets.choice(chars) for _ in range(lenght))

    return f"{prefix}-{get_chunck()}-{get_chunck()}-{get_chunck()}"