import bcrypt

from src.database import (
    conn,
    cursor
)

username = "admin"

password = "admin123"

hashed_password = bcrypt.hashpw(

    password.encode(),

    bcrypt.gensalt()
)

cursor.execute(

    """

    INSERT OR IGNORE INTO users (

        username,
        password,
        role,
        approved

    )

    VALUES (?, ?, ?, ?)

    """,

    (
        username,
        hashed_password,
        "admin",
        1
    )
)

conn.commit()

print("✅ Admin created successfully.")