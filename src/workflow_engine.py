from src.agents import (

    research_agent,

    summarization_agent,

    analytics_agent,

    planning_agent
)

# ===================================================
# AVAILABLE AGENTS
# ===================================================

AVAILABLE_AGENTS = {

    "Research Agent":
    research_agent,

    "Summarization Agent":
    summarization_agent,

    "Analytics Agent":
    analytics_agent,

    "Planning Agent":
    planning_agent
}

# ===================================================
# EXECUTE WORKFLOW
# ===================================================

def execute_workflow(

    user_task,

    selected_agents
):

    workflow_results = {}

    current_context = user_task

    # ---------------------------------------------------
    # RUN SELECTED AGENTS
    # ---------------------------------------------------

    for agent_name in selected_agents:

        agent_function = (
            AVAILABLE_AGENTS[
                agent_name
            ]
        )

        result = agent_function(
            current_context
        )

        workflow_results[
            agent_name
        ] = result

        # ---------------------------------------------------
        # PASS OUTPUT TO NEXT AGENT
        # ---------------------------------------------------

        current_context = result

    return workflow_results