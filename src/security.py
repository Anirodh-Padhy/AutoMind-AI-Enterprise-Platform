import jwt

import datetime

SECRET_KEY = "AUTOMIND_ENTERPRISE_SECRET"

ALGORITHM = "HS256"

# ===================================================
# CREATE JWT TOKEN
# ===================================================

def create_token(

    username,

    role
):

    payload = {

        "username": username,

        "role": role,

        "exp":

        datetime.datetime.utcnow()

        + datetime.timedelta(hours=12)
    }

    token = jwt.encode(

        payload,

        SECRET_KEY,

        algorithm=ALGORITHM
    )

    return token

# ===================================================
# VERIFY JWT TOKEN
# ===================================================

def verify_token(token):

    try:

        payload = jwt.decode(

            token,

            SECRET_KEY,

            algorithms=[ALGORITHM]
        )

        return payload

    except:

        return None