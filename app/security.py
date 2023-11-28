import datetime
import uuid

import jwt

SECRET_KEY = "mysecretkey"


def generate_jwt_for(target_id):
    token_id = uuid.uuid4()
    return jwt.encode(
        {
            "sub": target_id,
            "jti": str(token_id),
            "iss": "http://test.com/issuer",
            "iat": datetime.datetime.now(),
        },
        SECRET_KEY,
        algorithm="HS512",
    )


def decode_jwt_token(token):
    return jwt.decode(token, SECRET_KEY, algorithms=["HS512"])
