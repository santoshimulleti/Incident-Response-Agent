import os
import streamlit as st
from dotenv import load_dotenv
from groq import Groq
from hindsight_client import Hindsight

# =========================================================
# CONFIGURATION
# =========================================================

load_dotenv()

HINDSIGHT_API_KEY = os.getenv("HINDSIGHT_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

BANK_ID = "incident-response-agent"
GROQ_MODEL = "openai/gpt-oss-120b"

st.set_page_config(
    page_title="Incident Response Agent",
    page_icon="🛡️",
    layout="wide"
)

# =========================================================
# SESSION STATE
# =========================================================

defaults = {
    "before_result": "",
    "after_result": "",
    "after_memories": [],
    "recommendation": "",
    "memories": [],
    "incident_data": {},
    "resolution": "",
    "saved": False,
    "total_incidents": 0,
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

# =========================================================
# API KEY CHECK
# =========================================================

if not HINDSIGHT_API_KEY:
    st.error("HINDSIGHT_API_KEY is missing from .env")
    st.stop()

if not GROQ_API_KEY:
    st.error("GROQ_API_KEY is missing from .env")
    st.stop()

# =========================================================
# CLIENTS
# =========================================================

try:
    groq_client = Groq(api_key=GROQ_API_KEY)

    hindsight_client = Hindsight(
        base_url="https://api.hindsight.vectorize.io",
        api_key=HINDSIGHT_API_KEY
    )

except Exception as e:
    st.error(f"Connection error: {e}")
    st.stop()

# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.title("🛡️ Incident Response")

    st.success("🧠 Hindsight Connected")
    st.success("🤖 Groq Connected")

    st.divider()

    st.subheader("⚙️ How It Works")

    st.markdown("""
    **1️⃣ Report**  
    Submit a security incident.

    **2️⃣ Recall**  
    Hindsight searches previous incidents.

    **3️⃣ Reason**  
    Groq analyzes the incident using memory.

    **4️⃣ Resolve**  
    Investigate and resolve the incident.

    **5️⃣ Retain**  
    The new resolution is stored for future incidents.
    """)

    st.divider()

    st.caption(
        "AI-assisted incident investigation powered by persistent memory."
    )

# =========================================================
# HEADER
# =========================================================

st.title("🛡️ Incident Response Agent")

st.caption(
    "AI-powered incident investigation with persistent memory"
)

st.markdown(
    """
    Investigate security incidents using **Groq AI** and **Hindsight
    long-term memory**. The agent recalls similar incidents, learns from
    previous resolutions, and improves future investigations.
    """
)

st.divider()

# =========================================================
# STATUS CARDS
# =========================================================

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "🧠 Hindsight Memories",
        "10+"
    )

with col2:
    st.metric(
        "🚨 Incidents Processed",
        st.session_state.total_incidents
    )

with col3:
    st.metric(
        "🤖 AI Engine",
        "Groq"
    )

st.divider()

# =========================================================
# HOW THE AGENT LEARNS
# =========================================================

st.subheader("🧠 How the Agent Learns")

st.caption(
    "The agent continuously improves by recalling and retaining incident knowledge."
)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### 🔎 Recall")
    st.write(
        "Hindsight retrieves relevant incidents and resolutions "
        "from previous investigations."
    )

with col2:
    st.markdown("### 🧠 Reason")
    st.write(
        "Groq analyzes the current incident together with "
        "the recalled memory."
    )

with col3:
    st.markdown("### 💾 Retain")
    st.write(
        "The final incident resolution is stored so it can "
        "help with future incidents."
    )

st.divider()

# =========================================================
# BEFORE VS AFTER HINDSIGHT
# =========================================================

st.subheader("🔬 Before vs After Hindsight")

st.caption(
    "See how persistent memory improves incident investigation."
)

demo_title = st.text_input(
    "Demo Incident",
    value="Database Connection Failure"
)

demo_description = st.text_area(
    "Demo Description",
    value=(
        "Users are unable to connect to the production database "
        "after a recent network configuration change."
    )
)

col1, col2 = st.columns(2)

# ---------------------------------------------------------
# WITHOUT HINDSIGHT
# ---------------------------------------------------------

with col1:

    st.markdown("### 🟠 Without Hindsight")

    if st.button(
        "Analyze Without Hindsight",
        use_container_width=True
    ):

        prompt = f"""
You are a cybersecurity incident response assistant.

Analyze the following incident WITHOUT using previous incident memory.

Incident:
{demo_title}

Description:
{demo_description}

Provide:
1. Possible root causes
2. Investigation steps
3. Recommended immediate actions

Keep the answer concise and practical.
"""

        try:

            response = groq_client.chat.completions.create(
                model=GROQ_MODEL,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.2,
                max_tokens=450
            )

            st.session_state.before_result = (
                response.choices[0].message.content
            )

        except Exception as e:
            st.error(f"AI error: {e}")

    if st.session_state.before_result:

        st.info(st.session_state.before_result)

# ---------------------------------------------------------
# WITH HINDSIGHT
# ---------------------------------------------------------

with col2:

    st.markdown("### 🟢 With Hindsight")

    if st.button(
        "Analyze With Hindsight",
        use_container_width=True
    ):

        try:

            recall_result = hindsight_client.recall(
                bank_id=BANK_ID,
                query=demo_description
            )

            memories = recall_result.results or []

            st.session_state.after_memories = memories

            memory_text = "\n\n".join(
                [
                    memory.text
                    for memory in memories[:5]
                ]
            )

            if not memory_text:
                memory_text = "No previous relevant incidents were found."

            prompt = f"""
You are a cybersecurity incident response assistant.

Analyze the current incident using the previous incident
memories retrieved from Hindsight.

CURRENT INCIDENT:
Title:
{demo_title}

Description:
{demo_description}

PREVIOUS INCIDENT MEMORIES:
{memory_text}

Provide:
1. Likely root cause based on current evidence and previous incidents
2. Investigation steps
3. Recommended immediate actions
4. Explain how previous incidents influenced the analysis

Do not claim certainty when the evidence is insufficient.

Keep the answer concise and practical.
"""

            response = groq_client.chat.completions.create(
                model=GROQ_MODEL,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.2,
                max_tokens=450
            )

            st.session_state.after_result = (
                response.choices[0].message.content
            )

        except Exception as e:
            st.error(f"Hindsight/AI error: {e}")

    if st.session_state.after_result:

        st.success(
            f"🧠 Hindsight recalled "
            f"{len(st.session_state.after_memories)} "
            f"previous incident(s)."
        )

        st.info(st.session_state.after_result)

st.divider()

# =========================================================
# REPORT NEW INCIDENT
# =========================================================

st.subheader("🚨 Report New Incident")

st.caption(
    "Submit an incident and let Hindsight recall relevant past incidents "
    "to support the investigation."
)

with st.form("incident_form"):

    incident_title = st.text_input(
        "Incident Title",
        placeholder="Example: Database Server Connectivity Failure"
    )

    col1, col2 = st.columns(2)

    with col1:

        severity = st.selectbox(
            "Severity",
            [
                "Low",
                "Medium",
                "High",
                "Critical"
            ]
        )

    with col2:

        affected_system = st.text_input(
            "Affected System",
            placeholder="Example: Production Database"
        )

    description = st.text_area(
        "Incident Description",
        placeholder=(
            "Describe what happened, when it happened, "
            "and what users or systems are affected."
        ),
        height=150
    )

    analyze_button = st.form_submit_button(
        "🔎 Analyze Incident",
        use_container_width=True
    )

# =========================================================
# INCIDENT ANALYSIS
# =========================================================

if analyze_button:

    if not incident_title or not affected_system or not description:

        st.warning(
            "Please fill in the incident title, affected system, "
            "and description."
        )

    else:

        st.session_state.incident_data = {
            "title": incident_title,
            "severity": severity,
            "affected_system": affected_system,
            "description": description
        }

        st.session_state.saved = False

        with st.spinner(
            "🧠 Recalling previous incidents from Hindsight..."
        ):

            try:

                recall_result = hindsight_client.recall(
                    bank_id=BANK_ID,
                    query=description
                )

                memories = recall_result.results or []

                st.session_state.memories = memories

            except Exception as e:

                st.error(
                    f"Could not retrieve Hindsight memories: {e}"
                )

                st.session_state.memories = []

        # -------------------------------------------------
        # DISPLAY MEMORIES
        # -------------------------------------------------

        st.subheader("🧠 Relevant Previous Incidents")

        if st.session_state.memories:

            st.success(
                f"Hindsight recalled "
                f"{len(st.session_state.memories)} "
                f"relevant incident(s)."
            )

            for i, memory in enumerate(
                st.session_state.memories[:5],
                start=1
            ):

                with st.expander(
                    f"Previous Incident {i}"
                ):

                    st.write(memory.text)

        else:

            st.info(
                "No closely related previous incidents were found."
            )

        # -------------------------------------------------
        # BUILD MEMORY TEXT
        # -------------------------------------------------

        memory_text = "\n\n".join(
            [
                memory.text
                for memory in st.session_state.memories[:5]
            ]
        )

        if not memory_text:

            memory_text = (
                "No previous incident memories were found."
            )

        # -------------------------------------------------
        # AI ANALYSIS
        # -------------------------------------------------

        with st.spinner(
            "🤖 Groq is analyzing the incident using Hindsight memory..."
        ):

            prompt = f"""
You are an expert cybersecurity incident response assistant.

Analyze the following security incident using the previous
incident memories retrieved from Hindsight.

CURRENT INCIDENT:

Title:
{incident_title}

Severity:
{severity}

Affected System:
{affected_system}

Description:
{description}

PREVIOUS INCIDENT MEMORIES:

{memory_text}

Provide a concise incident response recommendation with:

1. Possible root cause
2. Investigation steps
3. Immediate recommended actions
4. Relevant previous incident or lesson
5. Confidence level

Use previous memories as supporting context.
Do not claim certainty when the evidence is insufficient.
"""

            try:

                response = groq_client.chat.completions.create(
                    model=GROQ_MODEL,
                    messages=[
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    temperature=0.2,
                    max_tokens=600
                )

                st.session_state.recommendation = (
                    response.choices[0].message.content
                )

                st.session_state.total_incidents += 1

            except Exception as e:

                st.error(
                    f"AI analysis failed: {e}"
                )

# =========================================================
# AI RECOMMENDATION
# =========================================================

if st.session_state.recommendation:

    st.subheader("🤖 AI Incident Analysis")

    st.info(
        st.session_state.recommendation
    )

# =========================================================
# SAVE INCIDENT MEMORY
# =========================================================

if st.session_state.incident_data:

    st.divider()

    st.subheader("💾 Save Incident Knowledge")

    st.caption(
        "Enter the final resolution so Hindsight can learn from this incident."
    )

    resolution_input = st.text_area(
        "Incident Resolution / Outcome",
        value=st.session_state.resolution,
        placeholder=(
            "Example: Firewall rules were reviewed and updated. "
            "Database connectivity was restored successfully."
        ),
        height=130
    )

    if st.button(
        "💾 Save Incident Memory",
        use_container_width=True
    ):

        if not resolution_input.strip():

            st.warning(
                "Please enter the incident resolution before saving."
            )

        else:

            st.session_state.resolution = resolution_input

            incident = st.session_state.incident_data

            memory_content = f"""
Incident Title: {incident['title']}

Severity: {incident['severity']}

Affected System: {incident['affected_system']}

Incident Description:
{incident['description']}

AI Analysis:
{st.session_state.recommendation}

Resolution / Outcome:
{resolution_input}

This incident was investigated and resolved as part of the
Incident Response Agent workflow.
"""

            try:

                with st.spinner(
                    "💾 Storing incident knowledge in Hindsight..."
                ):

                    hindsight_client.retain(
                        bank_id=BANK_ID,
                        content=memory_content
                    )

                st.session_state.saved = True

                st.success(
                    "✅ Incident successfully stored in Hindsight memory."
                )

            except Exception as e:

                st.error(
                    f"Could not save incident memory: {e}"
                )

# =========================================================
# LEARNING COMPLETE
# =========================================================

if st.session_state.saved:

    st.divider()

    st.success(
        "🧠 Memory Learning Complete — this incident can now help future investigations."
    )

    st.markdown(
        """
        **Recall → Reason → Resolve → Retain**

        The agent has learned from this incident and its resolution.
        Future incidents can use this knowledge through Hindsight.
        """
    )

# =========================================================
# FOOTER
# =========================================================

st.divider()

st.caption(
    "🛡️ Incident Response Agent • "
    "Powered by Hindsight + Groq • "
    "Persistent AI Memory"
)

# =========================================================
# CLEANUP
# =========================================================

try:
    hindsight_client.close()
except Exception:
    pass