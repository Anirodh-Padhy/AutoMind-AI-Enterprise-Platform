from src.database import (
    conn,
    cursor
)

# ===================================================
# SAVE MEMORY
# ===================================================

def save_memory(

    username,

    memory_type,

    memory_content
):

    cursor.execute(

        """

        INSERT INTO ai_memory (

            username,
            memory_type,
            memory_content

        )

        VALUES (?, ?, ?)

        """,

        (
            username,
            memory_type,
            memory_content
        )
    )

    conn.commit()

# ===================================================
# LOAD MEMORY
# ===================================================

def load_memory(username):

    cursor.execute(

        """

        SELECT memory_type,
               memory_content,
               created_at

        FROM ai_memory

        WHERE username=?

        ORDER BY created_at DESC

        """,

        (username,)
    )

    results = cursor.fetchall()

    memory_items = []

    for row in results:

        memory_items.append({

            "memory_type": row[0],

            "memory_content": row[1],

            "created_at": row[2]
        })

    return memory_items