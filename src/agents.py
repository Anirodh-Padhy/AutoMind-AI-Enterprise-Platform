import ollama

# ===================================================
# BASE AGENT FUNCTION
# ===================================================

def run_agent(

    role,

    task,

    context=""
):

    try:

        prompt = f"""

        You are an AI agent.

        AGENT ROLE:
        {role}

        TASK:
        {task}

        CONTEXT:
        {context}

        Provide a professional response.
        """

        response = ollama.chat(

            model="phi3",

            messages=[

                {
                    "role": "user",

                    "content": prompt
                }
            ]
        )

        return response[
            "message"
        ][
            "content"
        ]

    except Exception as e:

        return f"Error: {str(e)}"

# ===================================================
# RESEARCH AGENT
# ===================================================

def research_agent(task):

    return run_agent(

        "Research Specialist",

        f"""
        Research this topic deeply:
        {task}

        Provide:
        - overview
        - important insights
        - major points
        """
    )

# ===================================================
# SUMMARIZATION AGENT
# ===================================================

def summarization_agent(

    research_output
):

    return run_agent(

        "Summarization Specialist",

        f"""
        Summarize this research clearly.

        CONTENT:
        {research_output}

        Provide:
        - concise summary
        - key points
        - important conclusions
        """
    )

# ===================================================
# ANALYTICS AGENT
# ===================================================

def analytics_agent(

    research_output
):

    return run_agent(

        "Analytics Specialist",

        f"""
        Analyze this information.

        CONTENT:
        {research_output}

        Provide:
        - trends
        - insights
        - opportunities
        - risks
        """
    )

# ===================================================
# PLANNING AGENT
# ===================================================

def planning_agent(

    research_output
):

    return run_agent(

        "Strategic Planning Specialist",

        f"""
        Create an action plan.

        CONTENT:
        {research_output}

        Provide:
        - step-by-step strategy
        - execution roadmap
        - recommendations
        """
    )

# ===================================================
# MULTI-AGENT ORCHESTRATION
# ===================================================

def run_multi_agent_workflow(

    user_task
):

    # ---------------------------------------------------
    # STEP 1 — RESEARCH
    # ---------------------------------------------------

    research = research_agent(
        user_task
    )

    # ---------------------------------------------------
    # STEP 2 — SUMMARY
    # ---------------------------------------------------

    summary = summarization_agent(
        research
    )

    # ---------------------------------------------------
    # STEP 3 — ANALYTICS
    # ---------------------------------------------------

    analytics = analytics_agent(
        research
    )

    # ---------------------------------------------------
    # STEP 4 — PLANNING
    # ---------------------------------------------------

    planning = planning_agent(
        research
    )

    # ---------------------------------------------------
    # FINAL RESULT
    # ---------------------------------------------------

    final_result = f"""

# 🔍 Research Findings

{research}

---

# 📝 Summary

{summary}

---

# 📊 Analytics Insights

{analytics}

---

# 📅 Strategic Plan

{planning}
"""

    return final_result