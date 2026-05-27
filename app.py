import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np

from src.auth import (

    register_user,

    login_user,

    get_pending_users,

    approve_user,

    delete_user,

    update_user_role,

    get_all_users
)

from src.agents import (
    run_multi_agent_workflow
)

from src.workflow_engine import (
    execute_workflow
)

from src.workflow_storage import (
    save_workflow,
    load_workflows,
    save_workflow_execution,
    load_workflow_executions
)

from src.pdf_loader import (
    extract_pdf_text
)

from src.embeddings import (
    create_vector_store,
    search_documents
)

from src.memory_manager import (
    save_memory,
    load_memory
)

from src.workspace_manager import (
    save_document,
    load_documents
)

from src.analytics_engine import (
    calculate_agent_usage,
    workflow_execution_analytics,
    productivity_metrics
)

from streamlit_autorefresh import (
    st_autorefresh
)

from src.scheduler_engine import (

    save_scheduled_workflow,

    load_scheduled_workflows,

    delete_scheduled_workflow
)

from src.security import (

    create_token,

    verify_token
)

# ===================================================
# PAGE CONFIG
# ===================================================

st.set_page_config(
    page_title="AutoMind AI",
    layout="wide"
)

# ===================================================
# SESSION STATE
# ===================================================

session_defaults = {

    "authenticated": False,
    "username": "",
    "role": "",
    "workflow_history": [],
    "saved_workflows": [],
    "document_text": "",
    "vector_index": None,
    "document_chunks": [],
    "workspace_memory": [],
    "saved_documents": []
}
if "token" not in st.session_state:

    st.session_state.token = None

for key, value in session_defaults.items():

    if key not in st.session_state:

        st.session_state[key] = value

# ===================================================
# CUSTOM CSS
# ===================================================

st.markdown("""

<style>

/* ===================================================
GLOBAL APP
=================================================== */

html, body, [class*="css"] {

    font-family: 'Segoe UI', sans-serif;
}

/* ===================================================
MAIN BACKGROUND
=================================================== */

.main {

    background:

    linear-gradient(

        135deg,

        #0B1120,

        #111827,

        #0F172A
    );

    color: white;
}

/* ===================================================
SIDEBAR
=================================================== */

section[data-testid="stSidebar"] {

    background:

    linear-gradient(

        180deg,

        #111827,

        #0F172A
    );

    border-right:

    1px solid rgba(255,255,255,0.08);
}

/* ===================================================
SIDEBAR TEXT
=================================================== */

section[data-testid="stSidebar"] * {

    color: white !important;
}

/* ===================================================
GLASS CONTAINER
=================================================== */

.glass-container {

    background:

    rgba(255,255,255,0.05);

    border:

    1px solid rgba(255,255,255,0.08);

    border-radius: 20px;

    padding: 25px;

    margin-bottom: 20px;

    backdrop-filter: blur(12px);

    box-shadow:

    0 8px 32px rgba(0,0,0,0.25);

    transition: 0.3s;
}

.glass-container:hover {

    transform: translateY(-3px);

    border:

    1px solid #8B5CF6;
}

/* ===================================================
METRIC CARDS
=================================================== */

.metric-card {

    background:

    rgba(255,255,255,0.05);

    border-radius: 20px;

    padding: 20px;

    text-align: center;

    border:

    1px solid rgba(255,255,255,0.08);

    backdrop-filter: blur(10px);

    box-shadow:

    0 4px 20px rgba(0,0,0,0.25);

    transition: 0.3s;
}

.metric-card:hover {

    transform: scale(1.02);

    border:

    1px solid #A78BFA;
}

/* ===================================================
BUTTONS
=================================================== */

.stButton>button {

    width: 100%;

    height: 3em;

    border-radius: 12px;

    border: none;

    font-weight: bold;

    color: white;

    background:

    linear-gradient(

        90deg,

        #7C3AED,

        #8B5CF6
    );

    transition: 0.3s;

    box-shadow:

    0 4px 15px rgba(124,58,237,0.3);
}

.stButton>button:hover {

    transform: scale(1.03);

    background:

    linear-gradient(

        90deg,

        #8B5CF6,

        #A78BFA
    );
}

/* ===================================================
INPUT FIELDS
=================================================== */

.stTextInput>div>div>input,

.stTextArea textarea,

.stSelectbox div[data-baseweb="select"] {

    background-color:

    rgba(255,255,255,0.05) !important;

    color: white !important;

    border-radius: 12px !important;

    border:

    1px solid rgba(255,255,255,0.1) !important;
}

/* ===================================================
HEADERS
=================================================== */

h1 {

    font-size: 3rem !important;

    font-weight: 800 !important;

    color: white !important;
}

h2, h3 {

    color: #E5E7EB !important;
}

/* ===================================================
SUCCESS ALERTS
=================================================== */

.stSuccess {

    border-radius: 15px;
}

/* ===================================================
INFO ALERTS
=================================================== */

.stInfo {

    border-radius: 15px;
}

/* ===================================================
WARNING ALERTS
=================================================== */

.stWarning {

    border-radius: 15px;
}

/* ===================================================
ERROR ALERTS
=================================================== */

.stError {

    border-radius: 15px;
}

/* ===================================================
EXPANDERS
=================================================== */

.streamlit-expanderHeader {

    background:

    rgba(255,255,255,0.03);

    border-radius: 10px;
}

/* ===================================================
SCROLLBAR
=================================================== */

::-webkit-scrollbar {

    width: 10px;
}

::-webkit-scrollbar-track {

    background: #111827;
}

::-webkit-scrollbar-thumb {

    background: #7C3AED;

    border-radius: 10px;
}

/* ===================================================
LIVE STATUS COLORS
=================================================== */

.status-live {

    color: #10B981;

    font-weight: bold;
}

.status-warning {

    color: #F59E0B;

    font-weight: bold;
}

.status-danger {

    color: #EF4444;

    font-weight: bold;
}

/* ===================================================
TABLES
=================================================== */

table {

    border-radius: 15px !important;

    overflow: hidden !important;
}

/* ===================================================
HOVER EFFECTS
=================================================== */

.element-container:hover {

    transition: 0.3s;
}

</style>

""", unsafe_allow_html=True)

# ===================================================
# AUTH PAGE
# ===================================================

if not st.session_state.authenticated:

    st.title("🤖 AutoMind AI")

    

    st.markdown(
        "## Multi-Agent AI Automation Platform"
    )

    auth_mode = st.sidebar.selectbox(

        "Authentication",

        [
            "Login",
            "Register"
        ]
    )

    username = st.text_input("Username")

    password = st.text_input(
        "Password",
        type="password"
    )

    # ===================================================
    # LOGIN
    # ===================================================

    if auth_mode == "Login":

        if st.button("Login"):

            success, message, role = login_user(
                username,
                password
            )

            if success:
                
                st.session_state.authenticated = True
                st.session_state.username = username
                st.session_state.role = role

                st.success(message)

                st.rerun()
            
            else:

                st.error(message)

    # ===================================================
    # REGISTER
    # ===================================================

    else:

        role = st.selectbox(

            "Select Role",

            [
                "user",
                "analyst"
            ]
        )

        if st.button("Register"):

            success, message = register_user(
                username,
                password,
                role
            )

            if success:

                st.success(message)
                
            else:

                st.error(message)
    
# ===================================================
# MAIN APP
# ===================================================

else:

    st.sidebar.success(
        f"Logged in as: {st.session_state.username}"
    )

    st.sidebar.info(
        f"Role: {st.session_state.role}"
    )

    # ===================================================
    # LOGOUT
    # ===================================================

    if st.sidebar.button("Logout"):

        st.session_state.authenticated = False
        st.session_state.username = ""
        st.session_state.role = ""
        st.session_state.workflow_history = []
        st.session_state.document_text = ""
        st.session_state.vector_index = None
        st.session_state.document_chunks = []

        st.rerun()

    # ===================================================
    # MENU
    # ===================================================

    menu_items = [

        "Dashboard",

        "AI Agents",

        "Workflow Automation",

        "Document Intelligence",

        "Workspace",

        "Autonomous Agents",

        "Analytics"
    ]

    if st.session_state.role == "admin":

        menu_items.append(
            "Admin Dashboard"
        )
    st.sidebar.markdown("""

    # 🚀 AutoMind AI

    ### Enterprise SaaS Platform

    ---
    """)
    menu = st.sidebar.radio(
        "Navigation",
        menu_items
    )

    # ===================================================
    # DASHBOARD
    # ===================================================

    if menu == "Dashboard":

        st.title(
            "🚀 AutoMind AI Enterprise Platform"
        )
        # ---------------------------------------------------
        # AUTO REFRESH
        # ---------------------------------------------------

        st_autorefresh(
        
            interval=5000,

            key="dashboard_refresh"
        )
        workflow_count = len(
            st.session_state.workflow_history
        )

        # ===================================================
        # TOTAL SCHEDULED WORKFLOWS
        # ===================================================

        total_scheduled = len(
        
            load_scheduled_workflows(
            
                st.session_state.username
            )
        )

        total_agents = 4

        total_saved_docs = len(

            load_documents(
                st.session_state.username
            )
        )

        total_memories = len(

            load_memory(
                st.session_state.username
            )
        )

        col1, col2, col3, col4, col5 = (
            st.columns(5)
        )

        with col1:

            st.metric(
                "AI Agents",
                total_agents
            )

        with col2:

            st.metric(
                "Workflows",
                workflow_count
            )

        with col3:

            st.metric(
                "Documents",
                total_saved_docs
            )

        with col4:

            st.metric(
                "AI Memories",
                total_memories
            )

        with col5:

            st.metric(
                "Autonomous Workflows",
                total_scheduled
            )  

        st.markdown("---")

        st.success(
            "Enterprise AI platform operational."
        )

        st.markdown("---")

        st.subheader(
            "⚡ Real-Time AI Monitoring"
        )

        # ---------------------------------------------------
        # LIVE METRICS
        # ---------------------------------------------------

        live_col1, live_col2, live_col3, live_col4 = (
            st.columns(4)
        )

        with live_col1:
        
            st.success(
                "🟢 AI Agents Online"
            )

        with live_col2:
        
            st.info(
                f"""
                ⚙️ Active Workflows:
                {workflow_count}
                """
            )

        with live_col3:
        
            st.warning(
                f"""
                🧠 Memory Records:
                {total_memories}
                """
            )

        with live_col4:
        
            st.success(
                "🚀 System Operational"
            )

        st.markdown("---")

        # ---------------------------------------------------
        # LIVE WORKFLOW FEED
        # ---------------------------------------------------

        st.subheader(
            "🕘 Live Workflow Feed"
        )

        if st.session_state[
            "workflow_history"
        ]:

            for workflow in reversed(
            
                st.session_state[
                    "workflow_history"
                ][-5:]
            ):

                st.markdown(f"""

                <div class="glass-container">

                <h4>
                ⚡ Workflow Executed
                </h4>

                <p>
                {workflow['task']}
                </p>

                </div>

                """, unsafe_allow_html=True)

        else:
        
            st.info(
                "No workflow activity yet."
            )

    # ===================================================
    # AI AGENTS
    # ===================================================

    elif menu == "AI Agents":

        st.title(
            "🤖 Multi-Agent AI System"
        )

        st.markdown(
            "### Enterprise AI Agent Orchestration Platform"
        )

        col1, col2, col3, col4 = st.columns(4)

        with col1:

            st.info("🔍 Research Agent")

        with col2:

            st.info("📝 Summary Agent")

        with col3:

            st.info("📊 Analytics Agent")

        with col4:

            st.info("📅 Planning Agent")

        st.markdown("---")

        user_task = st.text_area(

            "Describe Your AI Workflow Task",

            placeholder="""
Research AI startups and create
a business growth strategy
"""
        )

        if st.button(
            "🚀 Run Multi-Agent Workflow"
        ):

            if not user_task.strip():

                st.warning(
                    "Please enter a task."
                )

            else:

                with st.spinner(
                    "AI agents are collaborating..."
                ):

                    result = (
                        run_multi_agent_workflow(
                            user_task
                        )
                    )

                    st.session_state[
                        "workflow_history"
                    ].append({

                        "task": user_task,

                        "agents": [

                            "Research Agent",

                            "Summarization Agent",

                            "Analytics Agent",

                            "Planning Agent"
                        ],

                        "results": {

                            "Final Result": result
                        }
                    })

                st.success(
                    "Workflow completed successfully."
                )

                st.markdown("---")

                st.markdown(result)

        if st.session_state.workflow_history:

            st.markdown("---")

            st.subheader(
                "🕘 Workflow History"
            )

            for workflow in reversed(
                st.session_state.workflow_history
            ):

                with st.expander(
                    workflow["task"]
                ):

                    st.markdown(
                        workflow["results"][
                            "Final Result"
                        ]
                    )

            st.markdown("---")

            st.subheader(
                "🏢 Enterprise System Status"
            )

            status1, status2, status3 = st.columns(3)

            with status1:
            
                st.markdown("""

                <div class="glass-container">

                <h4 class="status-live">
                🟢 AI Orchestration
                </h4>

                <p>
                Operational
                </p>

                </div>

                """, unsafe_allow_html=True)

            with status2:
            
                st.markdown("""

                <div class="glass-container">

                <h4 class="status-live">
                🟢 Workflow Engine
                </h4>

                <p>
                Running Normally
                </p>

                </div>

                """, unsafe_allow_html=True)

            with status3:
            
                st.markdown("""

                <div class="glass-container">

                <h4 class="status-warning">
                🧠 AI Memory System
                </h4>

                <p>
                Monitoring Active
                </p>

                </div>

                """, unsafe_allow_html=True)

    # ===================================================
    # WORKFLOW AUTOMATION
    # ===================================================

    elif menu == "Workflow Automation":

        st.title(
            "⚙️ AI Workflow Automation Engine"
        )

        st.markdown(
            "### Build Multi-Agent AI Pipelines"
        )

        workflow_name = st.text_input(
            "Workflow Name"
        )

        user_task = st.text_area(

            "Describe Your Automation Task",

            placeholder="""
Research AI startups and create
a business strategy roadmap
"""
        )

        selected_agents = st.multiselect(

            "Select AI Agents",

            [

                "Research Agent",

                "Summarization Agent",

                "Analytics Agent",

                "Planning Agent"
            ],

            default=[

                "Research Agent",

                "Summarization Agent"
            ]
        )

        st.markdown("---")

        col1, col2 = st.columns(2)

        # ===================================================
        # SAVE WORKFLOW
        # ===================================================

        with col1:

            if st.button(
                "💾 Save Workflow"
            ):

                if workflow_name.strip():

                    save_workflow(

                        st.session_state.username,

                        workflow_name,

                        selected_agents
                    )

                    st.success(
                        "Workflow saved successfully."
                    )

                else:

                    st.warning(
                        "Please enter workflow name."
                    )

        # ===================================================
        # RUN WORKFLOW
        # ===================================================

        with col2:

            if st.button(
                "🚀 Run Workflow"
            ):

                if not user_task.strip():

                    st.warning(
                        "Please enter a task."
                    )

                elif not selected_agents:

                    st.warning(
                        "Select at least one agent."
                    )

                else:

                    if not workflow_name.strip():

                        workflow_name = (
                            "Untitled Workflow"
                        )

                    with st.spinner(
                        "AI workflow executing..."
                    ):

                        results = execute_workflow(

                            user_task,

                            selected_agents
                        )

                    save_workflow_execution(

                        st.session_state.username,

                        workflow_name,

                        user_task,

                        selected_agents,

                        results
                    )

                    save_memory(

                        st.session_state.username,

                        "workflow",

                        user_task
                    )

                    st.session_state[
                        "workflow_history"
                    ].append({

                        "task": user_task,

                        "agents": selected_agents,

                        "results": results
                    })

                    st.success(
                        "Workflow executed successfully."
                    )

                    st.markdown("---")

                    for agent, output in results.items():

                        st.subheader(
                            f"🤖 {agent}"
                        )

                        st.write(output)

                        st.markdown("---")

        # ===================================================
        # SAVED WORKFLOWS
        # ===================================================

        st.markdown("---")

        st.subheader(
            "📂 Saved Workflows"
        )

        workflows = load_workflows(
            st.session_state.username
        )

        if workflows:

            for workflow in workflows:

                with st.expander(

                    workflow[
                        "workflow_name"
                    ]
                ):

                    st.write("Agents:")

                    for agent in workflow[
                        "agents"
                    ]:

                        st.write(
                            f"✅ {agent}"
                        )

        else:

            st.info(
                "No saved workflows yet."
            )

        # ===================================================
        # EXECUTION HISTORY
        # ===================================================

        st.markdown("---")

        st.subheader(
            "🕘 Workflow Execution History"
        )

        executions = load_workflow_executions(
            st.session_state.username
        )

        if executions:

            for execution in executions:

                with st.expander(

                    f"""
{execution['workflow_name']}
• {execution['created_at']}
"""
                ):

                    st.markdown(
                        "### 📌 Task"
                    )

                    st.write(
                        execution["task"]
                    )

                    st.markdown(
                        "### 🤖 Agents Used"
                    )

                    for agent in execution[
                        "agents"
                    ]:

                        st.write(
                            f"✅ {agent}"
                        )

                    st.markdown("---")

                    st.markdown(
                        "### 📊 Workflow Results"
                    )

                    for agent, output in execution[
                        "results"
                    ].items():

                        st.subheader(
                            f"🤖 {agent}"
                        )

                        st.write(output)

                        st.markdown("---")

        else:

            st.info(
                "No workflow executions yet."
            )

    # ===================================================
    # DOCUMENT INTELLIGENCE
    # ===================================================

    elif menu == "Document Intelligence":

        st.title(
            "📄 Enterprise Document Intelligence"
        )

        st.markdown(
            "### AI-Powered Knowledge Automation System"
        )

        uploaded_file = st.file_uploader(

            "Upload PDF Document",

            type=["pdf"]
        )
        
        if uploaded_file:

            # ===================================================
            # FILE SIZE CHECK
            # ===================================================

            if uploaded_file.size > 10 * 1024 * 1024:
            
                st.error(
                    "File too large. Max 10MB."
                )

                st.stop()

            document_text = extract_pdf_text(
                uploaded_file
            )

            st.session_state.document_text = (
                document_text
            )

            save_document(

                st.session_state.username,

                uploaded_file.name,

                document_text
            )

            index, chunks = create_vector_store(
                document_text
            )

            st.session_state.vector_index = index
            st.session_state.document_chunks = chunks

            st.success(
                f"Document uploaded: {uploaded_file.name}"
            )

            st.success(
                "AI knowledge base created successfully."
            )

            st.info(
                f"Chunks Indexed: {len(chunks)}"
            )

            st.markdown("---")

            st.subheader(
                "📖 Document Preview"
            )

            st.text_area(

                "Extracted Text",

                document_text[:3000],

                height=300
            )

        st.markdown("---")

        st.subheader(
            "🧠 Ask Questions From Documents"
        )

        user_question = st.text_area(
            "Ask Your Question"
        )

        if st.button(
            "🔍 Analyze Document"
        ):

            if not st.session_state.vector_index:

                st.warning(
                    "Please upload a document first."
                )

            else:

                with st.spinner(
                    "AI agents analyzing document..."
                ):

                    retrieved_chunks = (
                        search_documents(

                            user_question,

                            st.session_state.vector_index,

                            st.session_state.document_chunks
                        )
                    )

                    context = "\n\n".join(
                        retrieved_chunks
                    )

                    rag_task = f"""

Analyze this document context.

DOCUMENT CONTEXT:
{context}

USER QUESTION:
{user_question}

Provide:
- detailed analysis
- insights
- recommendations
- summary
"""

                    result = (
                        run_multi_agent_workflow(
                            rag_task
                        )
                    )

                st.success(
                    "Document analysis completed."
                )

                st.markdown("---")

                st.markdown(result)

    # ===================================================
    # WORKSPACE
    # ===================================================

    elif menu == "Workspace":

        st.title(
            "💼 Persistent AI Workspace"
        )

        st.markdown(
            "### Enterprise AI Memory & Workspace System"
        )

        documents = load_documents(
            st.session_state.username
        )

        memories = load_memory(
            st.session_state.username
        )

        executions = load_workflow_executions(
            st.session_state.username
        )

        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(
                "Saved Documents",
                len(documents)
            )

        with col2:

            st.metric(
                "AI Memories",
                len(memories)
            )

        with col3:

            st.metric(
                "Workflow Executions",
                len(executions)
            )

        st.markdown("---")

        # ===================================================
        # DOCUMENTS
        # ===================================================

        st.subheader(
            "📄 Saved Documents"
        )

        if documents:

            for doc in documents:

                with st.expander(

                    f"""
{doc['filename']}
• {doc['created_at']}
"""
                ):

                    st.text_area(

                        "Document Content",

                        doc["content"][:2000],

                        height=200
                    )

        else:

            st.info(
                "No saved documents."
            )

        st.markdown("---")

        # ===================================================
        # AI MEMORY
        # ===================================================

        st.subheader(
            "🧠 AI Memory"
        )

        if memories:

            for memory in memories:

                with st.expander(

                    f"""
{memory['memory_type']}
• {memory['created_at']}
"""
                ):

                    st.write(
                        memory["memory_content"]
                    )

        else:

            st.info(
                "No AI memory available."
            )

        st.markdown("---")

        # ===================================================
        # EXECUTION HISTORY
        # ===================================================

        st.subheader(
            "⚙️ Workflow Execution History"
        )

        if executions:

            for execution in executions:

                with st.expander(

                    f"""
{execution['workflow_name']}
• {execution['created_at']}
"""
                ):

                    st.write(
                        f"Task: {execution['task']}"
                    )

                    st.write(
                        "Agents Used:"
                    )

                    for agent in execution[
                        "agents"
                    ]:

                        st.write(
                            f"✅ {agent}"
                        )

        else:

            st.info(
                "No workflow history yet."
            )

    # ===================================================
    # AUTONOMOUS AI AGENTS
    # ===================================================

    elif menu == "Autonomous Agents":

        st.title(
            "🤖 Autonomous AI Agents"
        )

        st.markdown(
            """
            ### Enterprise AI Automation Scheduler
            """
        )

        # ---------------------------------------------------
        # SCHEDULE WORKFLOW
        # ---------------------------------------------------

        st.subheader(
            "⏰ Schedule AI Workflow"
        )

        workflow_name = st.text_input(
            "Workflow Name"
        )

        task = st.text_area(
            "Automation Task"
        )

        selected_agents = st.multiselect(

            "Select AI Agents",

            [

                "Research Agent",

                "Summarization Agent",

                "Analytics Agent",

                "Planning Agent"
            ]
        )

        schedule_type = st.selectbox(

            "Schedule Type",

            [

                "Daily",

                "Weekly",

                "Monthly"
            ]
        )

        # ---------------------------------------------------
        # SAVE SCHEDULED WORKFLOW
        # ---------------------------------------------------

        if st.button(
            "💾 Schedule Workflow"
        ):

            if not workflow_name.strip():

                st.warning(
                    "Enter workflow name."
                )

            elif not task.strip():

                st.warning(
                    "Enter automation task."
                )

            elif not selected_agents:

                st.warning(
                    "Select at least one agent."
                )

            else:

                save_scheduled_workflow(

                    st.session_state[
                        "username"
                    ],

                    workflow_name,

                    task,

                    selected_agents,

                    schedule_type
                )

                st.success(
                    "Workflow scheduled successfully."
                )

        st.markdown("---")

        # ---------------------------------------------------
        # ACTIVE SCHEDULED WORKFLOWS
        # ---------------------------------------------------

        st.subheader(
            "⚡ Active Autonomous Workflows"
        )

        workflows = load_scheduled_workflows(

            st.session_state[
                "username"
            ]
        )

        if workflows:

            for workflow in workflows:

                with st.expander(

                    f"""
                    🤖
                    {workflow['workflow_name']}
                    •
                    {workflow['schedule_type']}
                    """
                ):

                    st.write(
                        f"""
                        Task:
                        {workflow['task']}
                        """
                    )

                    st.write(
                        "Agents:"
                    )

                    for agent in workflow[
                        "agents"
                    ]:

                        st.write(
                            f"✅ {agent}"
                        )

                    st.markdown("---")

                    # ---------------------------------------------------
                    # RUN AUTOMATION NOW
                    # ---------------------------------------------------

                    if st.button(

                        f"""
                        🚀 Run Now
                        """,

                        key=f"""
                        run_{workflow['id']}
                        """
                    ):

                        with st.spinner(
                            "Autonomous agents executing..."
                        ):

                            results = execute_workflow(

                                workflow["task"],

                                workflow["agents"]
                            )

                        # ---------------------------------------------------
                        # SAVE EXECUTION
                        # ---------------------------------------------------

                        save_workflow_execution(

                            st.session_state[
                                "username"
                            ],

                            workflow[
                                "workflow_name"
                            ],

                            workflow[
                                "task"
                            ],

                            workflow[
                                "agents"
                            ],

                            results
                        )

                        # ---------------------------------------------------
                        # SAVE MEMORY
                        # ---------------------------------------------------

                        save_memory(

                            st.session_state[
                                "username"
                            ],

                            "autonomous_workflow",

                            workflow["task"]
                        )

                        st.success(
                            "Autonomous workflow executed."
                        )

                        for agent, output in results.items():

                            st.subheader(
                                f"🤖 {agent}"
                            )

                            st.write(output)

                    st.markdown("---")

                    # ---------------------------------------------------
                    # DELETE SCHEDULED WORKFLOW
                    # ---------------------------------------------------

                    if st.button(

                        f"""
                        🗑️ Delete Workflow
                        """,

                        key=f"""
                        delete_{workflow['id']}
                        """
                    ):

                        delete_scheduled_workflow(

                            workflow["id"]
                        )

                        st.success(
                            "Workflow deleted."
                        )

                        st.rerun()

        else:

            st.info(
                "No autonomous workflows scheduled."
            )

    # ===================================================
    # ANALYTICS
    # ===================================================

    elif menu == "Analytics":

        st.title(
            "📊 Enterprise AI Analytics Dashboard"
        )

        st.markdown(
            "### AI Operations & Automation Intelligence"
        )

        workflow_history = st.session_state[
            "workflow_history"
        ]

        metrics = productivity_metrics(
            workflow_history
        )

        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(

                "Executed Workflows",

                metrics[
                    "total_workflows"
                ]
            )

        with col2:

            st.metric(

                "Total Agent Usage",

                metrics[
                    "total_agents_used"
                ]
            )

        with col3:

            st.metric(
                "Avg Agents / Workflow",
                round(
                    metrics.get(
                        "avg_agents_per_workflow",
                        0
                    ),
                    2
                )
            )

        st.markdown("---")

        # ===================================================
        # AGENT ANALYTICS
        # ===================================================

        st.subheader(
            "🤖 Agent Usage Analytics"
        )

        if workflow_history:

            agent_df = calculate_agent_usage(
                workflow_history
            )

            usage_chart = px.bar(

                agent_df,

                x="Agent",

                y="Usage",

                title="AI Agent Usage Frequency"
            )

            st.plotly_chart(
                usage_chart,
                use_container_width=True
            )

        else:

            st.info(
                "No workflow data available."
            )

        st.markdown("---")

        # ===================================================
        # EXECUTION TRENDS
        # ===================================================

        st.subheader(
            "⚙️ Workflow Execution Trends"
        )

        if workflow_history:

            workflow_df = (
                workflow_execution_analytics(
                    workflow_history
                )
            )

            workflow_df[
                "Execution"
            ] = range(

                1,

                len(workflow_df) + 1
            )

            workflow_df["Count"] = 1

            trend_chart = px.line(

                workflow_df,

                x="Execution",

                y="Count",

                markers=True,

                title="Workflow Execution Trend"
            )

            st.plotly_chart(
                trend_chart,
                use_container_width=True
            )

        else:

            st.info(
                "No workflow executions yet."
            )

        st.markdown("---")

        # ===================================================
        # COMPLEXITY ANALYTICS
        # ===================================================

        st.subheader(
            "📈 Workflow Complexity Analysis"
        )

        if workflow_history:

            complexity_data = []

            for workflow in workflow_history:

                complexity_data.append({

                    "Workflow":

                    workflow[
                        "task"
                    ][:30],

                    "Agents Used":

                    len(
                        workflow[
                            "agents"
                        ]
                    )
                })

            complexity_df = pd.DataFrame(
                complexity_data
            )

            complexity_chart = px.scatter(

                complexity_df,

                x="Workflow",

                y="Agents Used",

                size="Agents Used",

                title="Workflow Complexity"
            )

            st.plotly_chart(
                complexity_chart,
                use_container_width=True
            )

        else:

            st.info(
                "No complexity analytics available."
            )

        st.markdown("---")

        # ===================================================
        # AI INSIGHTS
        # ===================================================

        st.subheader(
            "🧠 AI Operational Insights"
        )

        if metrics[
            "total_workflows"
        ] >= 5:

            st.success(
                """
AI automation adoption
is increasing successfully.
"""
            )

        else:

            st.warning(
                """
Execute more workflows
to improve analytics accuracy.
"""
            )

        if metrics[
            "avg_agents_per_workflow"
        ] >= 3:

            st.info(
                """
Complex multi-agent orchestration
is actively being utilized.
"""
            )

        else:

            st.info(
                """
Workflow complexity is moderate.
Consider using more agents.
"""
            )

        st.markdown("---")

        st.subheader(
            "🏢 Enterprise Monitoring"
        )

        st.success(
            "System Status: Operational"
        )

        st.info(
            """
Multi-agent AI orchestration
running successfully.
"""
        )

        st.success(
            """
Workflow engine operating normally.
"""
        )

    # ===================================================
    # ADMIN DASHBOARD
    # ===================================================

    elif menu == "Admin Dashboard":

        st.title(
            "🛡️ Enterprise Admin Dashboard"
        )

        st.markdown(
            """
            ### User & Access Management
            """
        )

        # ---------------------------------------------------
        # CUSTOM CSS
        # ---------------------------------------------------

        st.markdown("""

        <style>

        .admin-card {

            background: #161B22;

            padding: 20px;

            border-radius: 15px;

            border: 1px solid #30363D;

            margin-bottom: 20px;
        }

        .admin-header {

            font-size: 20px;

            font-weight: bold;

            color: white;
        }

        .admin-sub {

            color: #8B949E;
        }

        .status-approved {

            color: #3FB950;

            font-weight: bold;
        }

        .status-pending {

            color: #D29922;

            font-weight: bold;
        }

        </style>

        """, unsafe_allow_html=True)

        # ---------------------------------------------------
        # PENDING APPROVALS
        # ---------------------------------------------------

        st.markdown("---")

        st.subheader(
            "⏳ Pending Approvals"
        )

        pending_users = get_pending_users()

        if pending_users:

            for user in pending_users:

                user_id = user[0]

                username = user[1]

                role = user[2]

                col1, col2 = st.columns([5,1])

                with col1:

                    st.markdown(f"""

                    <div class="admin-card">

                    <div class="admin-header">
                    👤 {username}
                    </div>

                    <div class="admin-sub">
                    Role: {role}
                    </div>

                    </div>

                    """, unsafe_allow_html=True)

                with col2:

                    st.write("")

                    if st.button(

                        "✅ Approve",

                        key=f"approve_{user_id}"
                    ):

                        approve_user(user_id)

                        st.success(
                            f"{username} approved."
                        )

                        st.rerun()

        else:

            st.success(
                "✅ No pending approvals"
            )

        # ---------------------------------------------------
        # USER MANAGEMENT
        # ---------------------------------------------------

        st.markdown("---")

        st.subheader(
            "👥 User Management"
        )

        users = get_all_users()

        # ---------------------------------------------------
        # TABLE HEADER
        # ---------------------------------------------------

        header1, header2, header3, header4, header5 = st.columns([2,2,2,2,3])

        header1.markdown("### User")
        header2.markdown("### Role")
        header3.markdown("### Status")
        header4.markdown("### Access")
        header5.markdown("### Actions")

        st.markdown("---")

        # ---------------------------------------------------
        # USER ROWS
        # ---------------------------------------------------

        for user in users:

            user_id = user[0]

            username = user[1]

            role = user[2]

            approved = user[3]

            status = (
                "Approved"
                if approved == 1
                else "Pending"
            )

            col1, col2, col3, col4, col5 = st.columns([2,2,2,2,3])

            # ---------------------------------------------------
            # USERNAME
            # ---------------------------------------------------

            with col1:

                st.markdown(f"""
                👤 **{username}**
                """)

            # ---------------------------------------------------
            # ROLE
            # ---------------------------------------------------

            with col2:

                if username == st.session_state[
                    "username"
                ]:

                    st.info("admin")

                else:

                    new_role = st.selectbox(

                        "Role",

                        [
                            "user",
                            "analyst",
                            "admin"
                        ],

                        index=[

                            "user",
                            "analyst",
                            "admin"

                        ].index(role),

                        key=f"role_{user_id}"
                    )

            # ---------------------------------------------------
            # STATUS
            # ---------------------------------------------------

            with col3:

                if approved == 1:

                    st.success("Approved")

                else:

                    st.warning("Pending")

            # ---------------------------------------------------
            # ACCESS
            # ---------------------------------------------------

            with col4:

                if role == "admin":

                    st.markdown(
                        "🛡️ Full Access"
                    )

                elif role == "analyst":

                    st.markdown(
                        "📊 Analytics Access"
                    )

                else:

                    st.markdown(
                        "👤 Standard Access"
                    )

            # ---------------------------------------------------
            # ACTIONS
            # ---------------------------------------------------

            with col5:

                action_col1, action_col2 = st.columns(2)

                # UPDATE ROLE

                with action_col1:

                    if username == st.session_state[
                        "username"
                    ]:

                        st.button(

                            "🔒 Locked",

                            disabled=True,

                            key=f"locked_{user_id}"
                        )

                    else:

                        if st.button(

                            "✏️ Update",

                            key=f"update_{user_id}"
                        ):

                            update_user_role(

                                user_id,

                                new_role
                            )

                            st.success(
                                f"{username} updated."
                            )

                            st.rerun()
                
                # DELETE USER

                with action_col2:

                    if username == st.session_state[
                        "username"
                    ]:

                        st.button(

                            "❌ Protected",

                            disabled=True,

                            key=f"protected_{user_id}"
                        )

                    else:

                        if st.button(

                            "🗑️ Delete",

                            key=f"delete_{user_id}"
                        ):

                            delete_user(user_id)

                            st.success(
                                f"{username} deleted."
                            )

                            st.rerun()

            st.markdown("---")

        # ---------------------------------------------------
        # ROLE DEFINITIONS
        # ---------------------------------------------------

        st.markdown("---")

        st.subheader(
            "ℹ️ Role Definitions"
        )

        role1, role2, role3 = st.columns(3)

        with role1:

            st.info(
                """
                🛡️ ADMIN

                Full platform access
                and user management.
                """
            )

        with role2:

            st.info(
                """
                📊 ANALYST

                Workflow creation
                and analytics access.
                """
            )

        with role3:

            st.info(
                """
                👤 USER

                Standard AI workflow
                access.
                """
            )