import streamlit as st
import json
from pathlib import Path
from datetime import datetime

from config import MAX_INTERVIEW_TURNS
from src.models import CandidateProfile
from src.orchestrator import InterviewOrchestrator

REPORTS_DIR = Path("saved_reports")
REPORTS_DIR.mkdir(exist_ok=True)

st.set_page_config(
    page_title="AI Technical Interview Coach",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("🎯 AI Technical Interview Coach")
st.caption("Adaptive multi-agent mock interview assistant powered by Gemini")

# Sidebar Configuration
st.sidebar.header("Candidate Setup")
candidate_name = st.sidebar.text_input("Candidate Name", value="Ronak")
target_role = st.sidebar.text_input("Target Role", value="AI Engineer")
focus_area = st.sidebar.text_input("Focus Area", value="System Design & LLM Engineering")
experience_level = st.sidebar.selectbox("Experience Level", ["Junior", "Mid-Level", "Senior", "Lead"], index=1)
resume_snippet = st.sidebar.text_area(
    "Resume Summary / Background",
    value="Built multi-agent LLM pipelines, experienced in Python, FastAPI, distributed systems.",
    height=120
)

# Initialize Session State
if "orchestrator" not in st.session_state:
    st.session_state.orchestrator = None
if "interview_started" not in st.session_state:
    st.session_state.interview_started = False
if "interview_finished" not in st.session_state:
    st.session_state.interview_finished = False
if "messages" not in st.session_state:
    st.session_state.messages = []
if "current_question" not in st.session_state:
    st.session_state.current_question = ""
if "final_report" not in st.session_state:
    st.session_state.final_report = ""

def start_interview():
    if not candidate_name.strip() or not target_role.strip():
        st.sidebar.error("Please fill Name and Target Role.")
        return
    
    profile = CandidateProfile(
        name=candidate_name,
        target_role=target_role,
        experience_level=experience_level,
        focus_area=focus_area,
        resume_snippet=resume_snippet
    )
    
    try:
        orch = InterviewOrchestrator(profile)
        opening_q = orch.start_interview()
        st.session_state.orchestrator = orch
        st.session_state.current_question = opening_q
        st.session_state.messages = [{"role": "assistant", "content": opening_q}]
        st.session_state.interview_started = True
        st.session_state.interview_finished = False
        st.session_state.final_report = ""
    except Exception as e:
        st.sidebar.error(f"Failed to start session: {str(e)}")

if not st.session_state.interview_started:
    if st.sidebar.button("🚀 Start Interview", use_container_width=True, type="primary"):
        start_interview()
        st.rerun()
    st.info("👈 Fill in your details on the sidebar and click **Start Interview** to begin.")
else:
    if st.sidebar.button("🔄 Reset / Start New Interview", use_container_width=True):
        st.session_state.interview_started = False
        st.session_state.interview_finished = False
        st.session_state.messages = []
        st.session_state.current_question = ""
        st.session_state.final_report = ""
        st.session_state.orchestrator = None
        st.rerun()

# Main Interview Screen
if st.session_state.interview_started and not st.session_state.interview_finished:
    current_turns = len(st.session_state.orchestrator.history)
    st.progress((current_turns) / MAX_INTERVIEW_TURNS, text=f"Turn {current_turns + 1} of {MAX_INTERVIEW_TURNS}")
    
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            
    col1, col2 = st.columns([1, 4])
    with col1:
        if st.button("🏁 Finish & Get Feedback", use_container_width=True):
            st.session_state.interview_finished = True
            st.rerun()

    user_input = st.chat_input("Type your response here...")
    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        try:
            with st.spinner("Evaluator Agent is assessing your answer..."):
                st.session_state.orchestrator.process_turn(
                    st.session_state.current_question,
                    user_input
                )
            
            turns_completed = len(st.session_state.orchestrator.history)
            if turns_completed >= MAX_INTERVIEW_TURNS:
                st.session_state.interview_finished = True
                st.rerun()
            else:
                with st.spinner("Interviewer Agent is framing the next question..."):
                    next_q = st.session_state.orchestrator.get_next_question()
                    st.session_state.current_question = next_q
                    st.session_state.messages.append({"role": "assistant", "content": next_q})
                st.rerun()
        except Exception as e:
            err = str(e)
            if "429" in err or "RESOURCE_EXHAUSTED" in err:
                st.warning("⚠️ API Rate limit reached. Wait 15 seconds and re-submit your response.")
            else:
                st.error(f"⚠️ Error: {err}")

# Final Report Screen
if st.session_state.interview_finished:
    st.success("🎉 Interview Completed!")
    
    if not st.session_state.final_report:
        with st.spinner("Coach Agent is preparing your personalized feedback report..."):
            try:
                report = st.session_state.orchestrator.generate_final_report()
                st.session_state.final_report = report
                
                # Save report
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"{candidate_name}_{target_role}_{timestamp}.md".replace(" ", "_")
                (REPORTS_DIR / filename).write_text(report, encoding="utf-8")
            except Exception as e:
                st.error(f"Failed to generate report: {str(e)}")

    if st.session_state.final_report:
        st.markdown(st.session_state.final_report)
        st.download_button(
            label="📥 Download Report (.md)",
            data=st.session_state.final_report,
            file_name=f"Interview_Report_{candidate_name}.md",
            mime="text/markdown"
        )
else:
    st.info("👈 Fill in your Candidate Name, Target Role, Background / Resume Snippet and Focus Area in the sidebar, then click **Start / Restart Interview** to begin!")