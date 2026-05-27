from src.database import (
    conn,
    cursor
)

# ===================================================
# SAVE DOCUMENT
# ===================================================

def save_document(

    username,

    filename,

    content
):

    cursor.execute(

        """

        INSERT INTO documents (

            username,
            filename,
            content

        )

        VALUES (?, ?, ?)

        """,

        (
            username,
            filename,
            content
        )
    )

    conn.commit()

# ===================================================
# LOAD DOCUMENTS
# ===================================================

def load_documents(username):

    cursor.execute(

        """

        SELECT filename,
               content,
               created_at

        FROM documents

        WHERE username=?

        ORDER BY created_at DESC

        """,

        (username,)
    )

    results = cursor.fetchall()

    documents = []

    for row in results:

        documents.append({

            "filename": row[0],

            "content": row[1],

            "created_at": row[2]
        })

    return documents