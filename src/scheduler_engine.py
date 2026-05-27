import json

from src.database import (
    conn,
    cursor
)

# ===================================================
# SAVE SCHEDULED WORKFLOW
# ===================================================

def save_scheduled_workflow(

    username,

    workflow_name,

    task,

    agents,

    schedule_type
):

    cursor.execute(

        """

        INSERT INTO scheduled_workflows (

            username,
            workflow_name,
            task,
            agents,
            schedule_type

        )

        VALUES (?, ?, ?, ?, ?)

        """,

        (

            username,

            workflow_name,

            task,

            json.dumps(agents),

            schedule_type
        )
    )

    conn.commit()

# ===================================================
# LOAD SCHEDULED WORKFLOWS
# ===================================================

def load_scheduled_workflows(username):

    cursor.execute(

        """

        SELECT id,
               workflow_name,
               task,
               agents,
               schedule_type,
               created_at

        FROM scheduled_workflows

        WHERE username=?

        ORDER BY created_at DESC

        """,

        (username,)
    )

    results = cursor.fetchall()

    workflows = []

    for row in results:

        workflows.append({

            "id": row[0],

            "workflow_name": row[1],

            "task": row[2],

            "agents": json.loads(row[3]),

            "schedule_type": row[4],

            "created_at": row[5]
        })

    return workflows

# ===================================================
# DELETE SCHEDULED WORKFLOW
# ===================================================

def delete_scheduled_workflow(workflow_id):

    cursor.execute(

        """

        DELETE FROM scheduled_workflows

        WHERE id=?

        """,

        (workflow_id,)
    )

    conn.commit()