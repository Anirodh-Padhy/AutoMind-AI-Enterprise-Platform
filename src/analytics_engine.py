import pandas as pd

from collections import Counter

# ===================================================
# AGENT USAGE ANALYTICS
# ===================================================

def calculate_agent_usage(

    workflow_history
):

    agent_counter = Counter()

    for workflow in workflow_history:

        for agent in workflow[
            "agents"
        ]:

            agent_counter[agent] += 1

    return pd.DataFrame({

        "Agent": list(
            agent_counter.keys()
        ),

        "Usage": list(
            agent_counter.values()
        )
    })

# ===================================================
# WORKFLOW EXECUTION ANALYTICS
# ===================================================

def workflow_execution_analytics(

    workflow_history
):

    workflow_names = []

    for workflow in workflow_history:

        workflow_names.append(

            workflow.get(
                "task",
                "Unknown"
            )[:30]
        )

    return pd.DataFrame({

        "Workflow": workflow_names
    })

# ===================================================
# PRODUCTIVITY METRICS
# ===================================================

def productivity_metrics(

    workflow_history
):

    total_workflows = len(
        workflow_history
    )

    total_agents_used = sum(

        len(
            workflow["agents"]
        )

        for workflow in workflow_history
    )

    avg_agents_per_workflow = 0

    if total_workflows > 0:

        avg_agents_per_workflow = (

            total_agents_used
            /
            total_workflows
        )

    return {

        "total_workflows":
        total_workflows,

        "total_agents_used":
        total_agents_used,

        "avg_agents_per_workflow":
        avg_agents_per_workflow
    }