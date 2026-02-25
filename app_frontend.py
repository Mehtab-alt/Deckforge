import streamlit as st
import requests
import time
import os

API_URL = os.getenv("API_URL", "http://api:8000")

# Simulate Auth (Phase 6)
st.sidebar.title("Login")
username = st.sidebar.text_input("Email")
if st.sidebar.button("Login"):
    st.session_state.token = username # Simulating JWT
    st.success(f"Logged in as {username}")

if "token" in st.session_state:
    st.title("DeckForge SaaS")
    
    idea = st.text_area("Infrastructure Idea")
    name = st.text_input("Project Name")
    
    if st.button("Forge (Cloud)"):
        headers = {"Authorization": f"Bearer {st.session_state.token}"}
        payload = {"idea": idea, "project_name": name}
        
        try:
            res = requests.post(f"{API_URL}/forge", json=payload, headers=headers)
            if res.status_code == 200:
                task_id = res.json()["task_id"]
                st.info(f"Task {task_id} queued on worker cluster.")
            else:
                st.error(f"Error: {res.text}")
        except Exception as e:
            st.error(f"Connection failed: {e}")

    # Phase 8: Data Flywheel Interface
    st.divider()
    st.subheader("🔧 Fine-Tune the AI")
    col1, col2 = st.columns(2)
    with col1:
        orig = st.text_area("Original AI Code", height=100)
    with col2:
        fix = st.text_area("Your Correction", height=100)
    
    if st.button("Submit Correction"):
        requests.post(
            f"{API_URL}/feedback", 
            json={"original": orig, "corrected": fix},
            headers={"Authorization": f"Bearer {st.session_state.token}"}
        )
        st.success("Thank you! The models will be retrained tonight.")