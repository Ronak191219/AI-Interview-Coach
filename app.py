import os
import json
from datetime import datetime
from pathlib import Path
import streamlit as st

from config import MAX_INTERVIEW_TURNS
from src.models import CandidateProfile
from src.orchestrator import InterviewOrchestrator

# Setup directory for saved reports
REPORTS_DIR = Path("saved_reports")
REPORTS_DIR.mkdir(exist_ok=True)

st.set_page_config(
    page_title="AI Mock Interview Coach (Gemini)",
    page_icon="🎙️",
    layout="wide"
)

st.title("🎙️ AI Mock Interview Coach (Powered by Google Gemini)")
st.caption("Adaptive multi-agent mock interview assistant powered by Gemini 2.5 Flash")

# Initialize Session State Variables
if "orchestrator" not in st.session_state:
    st.session_state.orchestrator = None
if "interview_started" not in st.session_state:
    st.session_state.interview_started = False
if "interview_finished" not in st.session_state:
    st.session_state.interview_finished = False
if "current_question" not in st.session_state:
    st.session_state.current_question = ""
if "messages" not in st.session_state:
    st.session_state.messages = []
if "coaching_report" not in st.session_state:
    st.session_state.coaching_report = ""
if "viewing_saved_report" not in st.session_state:
    st.session_state.viewing_saved_report = None

# Sidebar Configuration
st.sidebar.header("🎯 Candidate Profile")
candidate_name = st.sidebar.text_input("Candidate Name", value="Ronak")
target_role = st.sidebar.text_input("Target Role", value="AI Engineer")
candidate_background = st.sidebar.text_area(
    "Background / Resume Snippet", 
    value="3 years experience with Python, Machine Learning, Generative AI, FastAPI and MySQL."
)
focus_area = st.sidebar.selectbox(
    "Focus Area",
    options=["technical", "mixed", "behavioral", "case"]
)

start_button = st.sidebar.button("🚀 Start / Restart Interview", type="primary")

if start_button:
    # Handle Pydantic model field matching safely
    try:
        profile = CandidateProfile(
            name=candidate_name if candidate_name else "Candidate",
            target_role=target_role,
            background=candidate_background,
            focus_area=focus_area
        )
    except Exception:
        profile = CandidateProfile(
            candidate_name=candidate_name if candidate_name else "Candidate",
            target_role=target_role,
            candidate_background=candidate_background,
            focus_area=focus_area
        )

    with st.spinner("Connecting with Interviewer Agent..."):
        try:
            orchestrator = InterviewOrchestrator(profile)
            opening_question = orchestrator.start_interview()
            
            st.session_state.orchestrator = orchestrator
            st.session_state.interview_started = True
            st.session_state.interview_finished = False
            st.session_state.current_question = opening_question
            st.session_state.messages = [{"role": "assistant", "content": opening_question}]
            st.session_state.coaching_report = ""
            st.session_state.viewing_saved_report = None
            st.rerun()
        except Exception as e:
            st.error(f"Failed to start session: {e}")

# Sidebar Section for Saved Reports
st.sidebar.divider()
st.sidebar.header("📁 Saved Reports")

saved_files = sorted(list(REPORTS_DIR.glob("*.md")), reverse=True)

if saved_files:
    for file_path in saved_files:
        filename = file_path.stem
        display_label = f"📜 {filename[:28]}"
        if st.sidebar.button(display_label, key=str(file_path)):
            with open(file_path, "r", encoding="utf-8") as f:
                st.session_state.viewing_saved_report = f.read()
            st.session_state.interview_started = False
            st.rerun()
else:
    st.sidebar.caption("No saved reports yet.")

# Sidebar Download for README.md
st.sidebar.divider()
st.sidebar.header("📄 Project Documentation")
readme_path = Path("README.md")
if readme_path.exists():
    with open(readme_path, "r", encoding="utf-8") as f:
        readme_content = f.read()
    st.sidebar.download_button(
        label="📥 Download README.md",
        data=readme_content,
        file_name="README.md",
        mime="text/markdown"
    )

# Display Saved Report View
if st.session_state.viewing_saved_report:
    st.success("📂 Viewing Saved Report from Sidebar")
    st.markdown(st.session_state.viewing_saved_report)
    
    st.download_button(
        label="📥 Download This Saved Report (.md)",
        data=st.session_state.viewing_saved_report,
        file_name="Interview_Report.md",
        mime="text/markdown"
    )
    
    if st.button("⬅️ Back to Active Interview Setup"):
        st.session_state.viewing_saved_report = None
        st.rerun()

# Display Chat Interface
elif st.session_state.interview_started:
    st.subheader(f"Session: {target_role} ({focus_area.capitalize()} Focus) — Candidate: {candidate_name}")
    
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    # Handle Active Chat Turn
    if not st.session_state.interview_finished:
        current_turns = len(st.session_state.orchestrator.history)
        st.info(f"Turn {current_turns + 1} of {MAX_INTERVIEW_TURNS}")

        user_input = st.chat_input("Type your response here...")

        col1, col2 = st.columns([1, 5])
        with col1:
            if st.button("Finish & Get Feedback"):
                st.session_state.interview_finished = True
                st.rerun()

        if user_input:
            st.session_state.messages.append({"role": "user", "content": user_input})
            with st.spinner("AI evaluating your answer..."):
                try:
                    st.session_state.orchestrator.process_turn(
                        st.session_state.current_question,
                        user_input
                    )
                    
                    turns_completed = len(st.session_state.orchestrator.history)

                    if turns_completed >= MAX_INTERVIEW_TURNS:
                        st.session_state.interview_finished = True
                        st.rerun()
                    else:
                        with st.spinner("Interviewer Agent is deciding next question..."):
                            next_q = st.session_state.orchestrator.get_next_question()
                            st.session_state.current_question = next_q
                            st.session_state.messages.append({"role": "assistant", "content": next_q})
                        st.rerun()
                        
                except Exception as e:
                    err_msg = str(e)
                    if "429" in err_msg or "RESOURCE_EXHAUSTED" in err_msg:
                        st.error("⚠️ Gemini API Rate limit hit hui hai. 10-15 seconds ruk kar dobara answer submit karein.")
                    else:
                        st.error(f"⚠️ Error occurred: {err_msg}")

    # Generate and Display Final Coaching Report
    if st.session_state.interview_finished:
        st.success("🎉 Interview Completed!")
        
        if not st.session_state.coaching_report:
            with st.spinner("Coach Agent is building your feedback report..."):
                report = st.session_state.orchestrator.generate_final_report()
                st.session_state.coaching_report = report

                # Auto-save report on generation
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                clean_name = candidate_name.replace(" ", "_")
                clean_role = target_role.replace(" ", "_")
                save_filename = f"{clean_name}_{clean_role}_{timestamp}.md"
                with open(REPORTS_DIR / save_filename, "w", encoding="utf-8") as f:
                    f.write(report)
                
                st.rerun()

        st.divider()
        st.header("📊 Final Coaching Feedback Report")
        st.markdown(st.session_state.coaching_report)

        st.download_button(
            label="📥 Download Report (.md)",
            data=st.session_state.coaching_report,
            file_name=f"Interview_Report_{candidate_name.replace(' ', '_')}_{target_role.replace(' ', '_')}.md",
            mime="text/markdown"
        )
else:
    st.info("👈 Fill in your Candidate Name, Target Role, Background / Resume Snippet and Focus Area in the sidebar, then click **Start / Restart Interview** to begin!")