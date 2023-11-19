import jwt
from config import config


def get_info_from_token(token_string: str):
    try:
        token = jwt.decode(token_string, config.SECRET_KEY, algorithms=["HS256"])
    except Exception as e:
        return False
    return token
