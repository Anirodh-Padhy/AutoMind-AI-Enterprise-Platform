import json

from src.database import (
    conn,
    cursor
)

# ===================================================
# SAVE WORKFLOW TEMPLATE
# ===================================================

def save_workflow(

    username,

    workflow_name,

    agents
):

    agents_string = ",".join(agents)

    cursor.execute(

        """

        INSERT INTO saved_workflows (

            username,
            workflow_name,
            agents

        )

        VALUES (?, ?, ?)

        """,

        (
            username,
            workflow_name,
            agents_string
        )
    )

    conn.commit()

# ===================================================
# LOAD WORKFLOW TEMPLATES
# ===================================================

def load_workflows(username):

    cursor.execute(

        """

        SELECT workflow_name,
               agents

        FROM saved_workflows

        WHERE username=?

        """,

        (username,)
    )

    results = cursor.fetchall()

    workflows = []

    for row in results:

        workflows.append({

            "workflow_name": row[0],

            "agents": row[1].split(",")
        })

    return workflows

# ===================================================
# SAVE EXECUTION HISTORY
# ===================================================

def save_workflow_execution(

    username,

    workflow_name,

    task,

    agents,

    results
):

    cursor.execute(

        """

        INSERT INTO workflow_executions (

            username,
            workflow_name,
            task,
            agents,
            results

        )

        VALUES (?, ?, ?, ?, ?)

        """,

        (

            username,

            workflow_name,

            task,

            json.dumps(agents),

            json.dumps(results)
        )
    )

    conn.commit()

# ===================================================
# LOAD EXECUTION HISTORY
# ===================================================

def load_workflow_executions(

    username
):

    cursor.execute(

        """

        SELECT workflow_name,
               task,
               agents,
               results,
               created_at

        FROM workflow_executions

        WHERE username=?

        ORDER BY created_at DESC

        """,

        (username,)
    )

    results = cursor.fetchall()

    executions = []

    for row in results:

        executions.append({

            "workflow_name": row[0],

            "task": row[1],

            "agents": json.loads(row[2]),

            "results": json.loads(row[3]),

            "created_at": row[4]
        })

    return executions