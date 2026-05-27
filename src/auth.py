from passlib.hash import bcrypt

from src.database import (
    conn,
    cursor
)

# ===================================================
# REGISTER USER
# ===================================================

def register_user(

    username,

    password,

    role
):

    # ---------------------------------------------------
    # PASSWORD VALIDATION
    # ---------------------------------------------------

    if len(password) < 8:

        return (

            False,

            "Password must be at least 8 characters."
        )

    # ---------------------------------------------------
    # HASH PASSWORD
    # ---------------------------------------------------

    hashed_password = bcrypt.hash(password)

    try:

        cursor.execute(

            """

            INSERT INTO users (

                username,
                password,
                role

            )

            VALUES (?, ?, ?)

            """,

            (

                username,

                hashed_password,

                role
            )
        )

        conn.commit()

        return (

            True,

            "Registration successful. Waiting for admin approval."
        )

    except Exception:

        return (

            False,

            "Username already exists."
        )

# ===================================================
# LOGIN USER
# ===================================================

def login_user(

    username,

    password
):

    cursor.execute(

        """

        SELECT password,
               role,
               approved

        FROM users

        WHERE username=?

        """,

        (username,)
    )

    result = cursor.fetchone()

    if result:

        stored_password = result[0]

        role = result[1]

        approved = result[2]

        # ---------------------------------------------------
        # ADMIN APPROVAL CHECK
        # ---------------------------------------------------

        if not approved:

            return (

                False,

                "Account pending admin approval.",

                None
            )

        # ---------------------------------------------------
        # VERIFY PASSWORD
        # ---------------------------------------------------

        if bcrypt.verify(

            password,

            stored_password
        ):

            return (

                True,

                "Login successful.",

                role
            )

    return (

        False,

        "Invalid credentials.",

        None
    )

# ===================================================
# GET PENDING USERS
# ===================================================

def get_pending_users():

    cursor.execute(

        """

        SELECT id,
               username,
               role

        FROM users

        WHERE approved=0

        """
    )

    return cursor.fetchall()

# ===================================================
# APPROVE USER
# ===================================================

def approve_user(user_id):

    cursor.execute(

        """

        UPDATE users

        SET approved=1

        WHERE id=?

        """,

        (user_id,)
    )

    conn.commit()

# ===================================================
# DELETE USER
# ===================================================

def delete_user(user_id):

    cursor.execute(

        """

        DELETE FROM users

        WHERE id=?

        """,

        (user_id,)
    )

    conn.commit()

# ===================================================
# UPDATE USER ROLE
# ===================================================

def update_user_role(

    user_id,

    new_role
):

    cursor.execute(

        """

        UPDATE users

        SET role=?

        WHERE id=?

        """,

        (
            new_role,
            user_id
        )
    )

    conn.commit()

# ===================================================
# GET ALL USERS
# ===================================================

def get_all_users():

    cursor.execute(

        """

        SELECT id,
               username,
               role,
               approved

        FROM users

        ORDER BY id DESC

        """
    )

    return cursor.fetchall()