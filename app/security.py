import datetime
import uuid
from fastapi import HTTPException, status

import jwt

from config.env_var_config import SECRET_KEY

ALGORITHM = "HS512"


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
        algorithm=ALGORITHM,
    )


def decode_jwt_token(token):
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
