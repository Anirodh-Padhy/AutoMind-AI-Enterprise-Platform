import sqlite3

# ---------------------------------------------------
# DATABASE CONNECTION
# ---------------------------------------------------

conn = sqlite3.connect(
    "automind_ai.db",
    check_same_thread=False
)

cursor = conn.cursor()

# ---------------------------------------------------
# USERS TABLE
# ---------------------------------------------------

cursor.execute("""

CREATE TABLE IF NOT EXISTS users (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    username TEXT UNIQUE,

    password TEXT,

    role TEXT DEFAULT 'user',

    approved INTEGER DEFAULT 0
)

""")

# ---------------------------------------------------
# WORKFLOWS TABLE
# ---------------------------------------------------

cursor.execute("""

CREATE TABLE IF NOT EXISTS workflows (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    username TEXT,

    workflow_name TEXT,

    workflow_result TEXT
)

""")

conn.commit()

# ---------------------------------------------------
# SAVED WORKFLOWS TABLE
# ---------------------------------------------------

cursor.execute("""

CREATE TABLE IF NOT EXISTS saved_workflows (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    username TEXT,

    workflow_name TEXT,

    agents TEXT
)

""")

conn.commit()

# ---------------------------------------------------
# WORKFLOW EXECUTION HISTORY
# ---------------------------------------------------

cursor.execute("""

CREATE TABLE IF NOT EXISTS workflow_executions (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    username TEXT,

    workflow_name TEXT,

    task TEXT,

    agents TEXT,

    results TEXT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)

""")

conn.commit()

# ---------------------------------------------------
# AI MEMORY TABLE
# ---------------------------------------------------

cursor.execute("""

CREATE TABLE IF NOT EXISTS ai_memory (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    username TEXT,

    memory_type TEXT,

    memory_content TEXT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)

""")

# ---------------------------------------------------
# DOCUMENT STORAGE TABLE
# ---------------------------------------------------

cursor.execute("""

CREATE TABLE IF NOT EXISTS documents (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    username TEXT,

    filename TEXT,

    content TEXT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)

""")

conn.commit()

# ===================================================
# SCHEDULED WORKFLOWS
# ===================================================

cursor.execute("""

CREATE TABLE IF NOT EXISTS scheduled_workflows (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    username TEXT,

    workflow_name TEXT,

    task TEXT,

    agents TEXT,

    schedule_type TEXT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)

""")

conn.commit()