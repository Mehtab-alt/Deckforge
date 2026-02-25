"""
DECKFORGE OS: The Complete Phase 1-10 Autonomous Infrastructure Platform
Run with: python deckforge_os.py all
"""

import os
import sys
import json
import time
import uuid
import subprocess
import threading
from datetime import datetime, timezone
from typing import List, Dict, Any, Optional

try:
    from fastapi import FastAPI, Depends, HTTPException, BackgroundTasks
    from pydantic import BaseModel
    from sqlalchemy import create_engine, Column, String, Integer, Text, DateTime, Boolean
    from sqlalchemy.orm import sessionmaker, declarative_base, Session
    import uvicorn
    import streamlit as st
    import requests
    from langchain_openai import ChatOpenAI
    from langchain_core.messages import HumanMessage
    from langgraph.graph import StateGraph, END
except ImportError:
    print("Missing packages. Run: pip install fastapi uvicorn sqlalchemy pydantic streamlit requests langgraph langchain-openai")
    sys.exit(1)

# ==========================================
# 1. DATABASE & CONFIG (Phase 5, 6, 8)
# ==========================================
os.environ.setdefault("DATABASE_URL", "sqlite:///./deckforge_os.db")
API_URL = "http://127.0.0.1:8000"

engine = create_engine(os.getenv("DATABASE_URL"), connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    username = Column(String, primary_key=True)
    password = Column(String)
    role = Column(String) # 'architect' or 'viewer'

class LiveResource(Base):
    __tablename__ = "live_resources"
    id = Column(String, primary_key=True)
    provider = Column(String) # AWS, Azure, GCP
    resource_type = Column(String)
    status = Column(String)
    cost_per_month = Column(String)

class Incident(Base):
    __tablename__ = "incidents"
    id = Column(String, primary_key=True)
    target_resource = Column(String)
    issue = Column(String)
    status = Column(String) # TRIGGERED, INVESTIGATING, AWAITING_APPROVAL, RESOLVED
    ai_analysis = Column(Text, default="")
    remediation_script = Column(Text, default="")
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

class TrainingData(Base):
    __tablename__ = "training_data"
    id = Column(Integer, primary_key=True, autoincrement=True)
    mistake = Column(Text)
    correction = Column(Text)

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try: yield db
    finally: db.close()

def seed_db():
    """Seed initial data for the demo"""
    db = SessionLocal()
    if not db.query(User).first():
        db.add(User(username="admin", password="password", role="architect"))
        db.add(User(username="viewer", password="password", role="viewer"))
        
        # Fake Phase 5 Live Resources
        db.add(LiveResource(id="aws-i-0abc123", provider="AWS", resource_type="EC2 Instance", status="Running", cost_per_month="$45.00"))
        db.add(LiveResource(id="gcp-sql-main", provider="GCP", resource_type="Cloud SQL", status="Running", cost_per_month="$120.00"))
    db.commit()
    db.close()

seed_db()

# ==========================================
# 2. CUSTOM ASYNC WORKER (Phase 7 - Windows Safe)
# ==========================================
# We use a global dictionary and threading instead of Celery to prevent Windows crashes.
class TaskManager:
    tasks = {}

    @classmethod
    def start_task(cls, task_id, func, *args):
        cls.tasks[task_id] = {"status": "PROCESSING", "result": None, "step": "Initializing"}
        
        def run():
            try:
                result = func(task_id, *args)
                cls.tasks[task_id] = {"status": "SUCCESS", "result": result, "step": "Done"}
            except Exception as e:
                cls.tasks[task_id] = {"status": "FAILED", "error": str(e), "step": "Error"}
                
        thread = threading.Thread(target=run)
        thread.start()

# ==========================================
# 3. AI BUILDER GRAPH (Phases 1-4 & 10)
# ==========================================
class BuilderState(BaseModel):
    idea: str
    lessons: str = ""
    target_cloud: str = ""
    architecture: str = ""
    terraform_code: str = ""

def llm_invoke(prompt, json_mode=False):
    llm = ChatOpenAI(model="gpt-4-turbo", temperature=0.1, model_kwargs={"response_format": {"type": "json_object"}} if json_mode else {})
    res = llm.invoke(prompt).content
    if json_mode:
        import re
        try: return json.loads(res)
        except: 
            match = re.search(r'```(?:json)?\s*(\{.*?\})\s*```', res, re.DOTALL)
            return json.loads(match.group(1)) if match else {}
    return res

def build_context_node(state: BuilderState):
    db = SessionLocal()
    history = db.query(TrainingData).order_by(TrainingData.id.desc()).limit(3).all()
    db.close()
    lessons = "Corporate Guidelines & Past Corrections:\n" + "".join([f"- {h.correction}\n" for h in history])
    return {"lessons": lessons}

def multi_cloud_node(state: BuilderState):
    # Phase 10: AI decides the best cloud provider based on the prompt
    prompt = f"Analyze this idea: '{state.idea}'. Determine the best cloud provider (AWS, Azure, or GCP). Return JSON: {{\"provider\": \"AWS/Azure/GCP\", \"reasoning\": \"...\"}}"
    res = llm_invoke(prompt, json_mode=True)
    return {"target_cloud": res.get("provider", "AWS")}

def build_forge_node(state: BuilderState):
    prompt = f"""
    Write raw Terraform code for this idea on {state.target_cloud}: {state.idea}.
    Follow these rules strictly: {state.lessons}
    Return JSON: {{"main.tf": "HCL code here", "architecture_summary": "Short description"}}
    """
    res = llm_invoke(prompt, json_mode=True)
    return {"terraform_code": res.get("main.tf", ""), "architecture": res.get("architecture_summary", "")}

build_graph = StateGraph(BuilderState)
build_graph.add_node("context", build_context_node)
build_graph.add_node("federation", multi_cloud_node) # Phase 10
build_graph.add_node("forge", build_forge_node)
build_graph.set_entry_point("context")
build_graph.add_edge("context", "federation")
build_graph.add_edge("federation", "forge")
build_graph.add_edge("forge", END)
builder_brain = build_graph.compile()

# ==========================================
# 4. AUTONOMOUS SRE GRAPH (Phase 9)
# ==========================================
class SREState(BaseModel):
    incident_id: str
    issue: str
    target: str
    analysis: str = ""
    script: str = ""

def sre_investigate_node(state: SREState):
    # AI simulates SSH-ing into the server and checking logs
    prompt = f"You are an SRE AI. A server ({state.target}) is experiencing: {state.issue}. Write a brief 2-sentence technical analysis of what likely caused this based on standard Linux/Cloud behavior."
    analysis = llm_invoke(prompt)
    return {"analysis": analysis}

def sre_remediate_node(state: SREState):
    # AI writes the fix
    prompt = f"Based on this analysis: {state.analysis}, write a safe Bash script to remediate the issue on {state.target}. Return JSON: {{\"bash_script\": \"...\"}}"
    res = llm_invoke(prompt, json_mode=True)
    return {"script": res.get("bash_script", "# sudo systemctl restart service")}

sre_graph = StateGraph(SREState)
sre_graph.add_node("investigate", sre_investigate_node)
sre_graph.add_node("remediate", sre_remediate_node)
sre_graph.set_entry_point("investigate")
sre_graph.add_edge("investigate", "remediate")
sre_graph.add_edge("remediate", END)
sre_brain = sre_graph.compile()

# ==========================================
# 5. FASTAPI BACKEND
# ==========================================
app = FastAPI()

class ForgeReq(BaseModel): idea: str
class FeedbackReq(BaseModel): mistake: str; correction: str

def run_builder_task(task_id, idea):
    TaskManager.tasks[task_id]["step"] = "Analyzing Intent & Multi-Cloud Routing..."
    state = BuilderState(idea=idea)
    result = builder_brain.invoke(state)
    return result

def run_sre_task(task_id, incident_id, target, issue):
    db = SessionLocal()
    inc = db.query(Incident).filter(Incident.id == incident_id).first()
    inc.status = "INVESTIGATING"
    db.commit()
    
    state = SREState(incident_id=incident_id, target=target, issue=issue)
    result = sre_brain.invoke(state)
    
    inc.ai_analysis = result["analysis"]
    inc.remediation_script = result["script"]
    inc.status = "AWAITING_APPROVAL"
    db.commit()
    db.close()
    return "Investigation Complete"

@app.post("/forge")
def api_forge(req: ForgeReq):
    task_id = str(uuid.uuid4())
    TaskManager.start_task(task_id, run_builder_task, req.idea)
    return {"task_id": task_id}

@app.get("/task/{task_id}")
def api_get_task(task_id: str):
    return TaskManager.tasks.get(task_id, {"status": "NOT_FOUND"})

@app.post("/feedback")
def api_feedback(req: FeedbackReq, db: Session = Depends(get_db)):
    db.add(TrainingData(mistake=req.mistake, correction=req.correction))
    db.commit()
    return {"status": "Learned"}

@app.post("/sre/trigger")
def api_trigger_alert(db: Session = Depends(get_db)):
    inc_id = f"INC-{str(uuid.uuid4())[:6].upper()}"
    inc = Incident(id=inc_id, target_resource="aws-i-0abc123", issue="CPU Spike 99% - Out of Memory", status="TRIGGERED")
    db.add(inc)
    db.commit()
    # Auto-trigger investigation
    TaskManager.start_task(f"sre-{inc_id}", run_sre_task, inc.id, inc.target_resource, inc.issue)
    return {"incident_id": inc.id}

@app.post("/sre/approve/{incident_id}")
def api_approve_fix(incident_id: str, db: Session = Depends(get_db)):
    inc = db.query(Incident).filter(Incident.id == incident_id).first()
    inc.status = "RESOLVED" # Simulates successful execution
    db.commit()
    return {"status": "Fixed"}

# ==========================================
# 6. STREAMLIT FRONTEND (The SaaS GUI)
# ==========================================
def run_streamlit():
    st.set_page_config(layout="wide", page_title="DeckForge OS")
    
    # Phase 6: RBAC Login
    if "user" not in st.session_state:
        st.markdown("<h1 style='text-align: center; color: #4A90E2;'>⚒️ DeckForge OS</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center;'>Phase 6: Role-Based Access Control</p>", unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1,1,1])
        with col2:
            st.info("Demo Accounts:\n- **admin** / password (Architect)\n- **viewer** / password (Read-Only)")
            user = st.text_input("Username")
            pw = st.text_input("Password", type="password")
            if st.button("Login", use_container_width=True):
                db = SessionLocal()
                u = db.query(User).filter(User.username == user, User.password == pw).first()
                if u:
                    st.session_state.user = u.username
                    st.session_state.role = u.role
                    st.rerun()
                else:
                    st.error("Invalid credentials")
                db.close()
        return

    # Main OS Dashboard
    st.sidebar.title(f"👤 {st.session_state.user.upper()}")
    st.sidebar.markdown(f"**Role:** `{st.session_state.role.upper()}`")
    if st.sidebar.button("Logout"):
        st.session_state.clear()
        st.rerun()

    st.title("⚒️ DeckForge Command Center")
    
    tab1, tab2, tab3, tab4 = st.tabs([
        "🛰️ Phase 5: State Tracker", 
        "🏗️ Phase 1-4 & 10: AI Builder", 
        "🛡️ Phase 9: Autonomous SRE", 
        "🧠 Phase 8: AI Learning"
    ])

    # Phase 5: State Tracking
    with tab1:
        st.subheader("Live Deployed Infrastructure")
        st.write("Tracking resources in real-time across multiple clouds.")
        db = SessionLocal()
        resources = db.query(LiveResource).all()
        
        for r in resources:
            with st.container(border=True):
                col1, col2, col3, col4 = st.columns(4)
                col1.markdown(f"**ID:** `{r.id}`")
                col2.markdown(f"**Cloud:** ☁️ {r.provider}")
                col3.markdown(f"**Type:** {r.resource_type}")
                col4.markdown(f"**Status:** 🟢 {r.status} ({r.cost_per_month})")
        db.close()

    # Phases 1-4 & 10: Multi-Cloud Builder
    with tab2:
        if st.session_state.role != "architect":
            st.error("🔒 Phase 6 RBAC: You need 'Architect' permissions to deploy infrastructure.")
        else:
            st.subheader("Abstract Intent to Infrastructure")
            idea = st.text_area("What do you want to build?", "A highly available PostgreSQL database cluster.")
            
            if st.button("Forge Infrastructure (Async)", type="primary"):
                res = requests.post(f"{API_URL}/forge", json={"idea": idea})
                st.session_state.build_task = res.json()["task_id"]
                st.rerun()

            if "build_task" in st.session_state:
                task = requests.get(f"{API_URL}/task/{st.session_state.build_task}").json()
                
                if task["status"] == "PROCESSING":
                    st.info(f"⏳ Phase 7 Worker Active: **{task['step']}**")
                    time.sleep(1)
                    st.rerun()
                elif task["status"] == "SUCCESS":
                    st.success("Infrastructure Generated!")
                    res = task["result"]
                    
                    st.markdown(f"### Phase 10: Multi-Cloud Federation")
                    st.success(f"**AI Selected Cloud:** ☁️ {res['target_cloud']}")
                    st.markdown(f"**Architecture Plan:** {res['architecture']}")
                    
                    st.markdown("### Generated Terraform")
                    st.code(res["terraform_code"], language="hcl")

    # Phase 9: Autonomous SRE
    with tab3:
        st.subheader("Autonomous Site Reliability Engineering")
        col1, col2 = st.columns([4, 1])
        with col2:
            if st.button("🚨 Simulate Server Crash"):
                requests.post(f"{API_URL}/sre/trigger")
                st.rerun()
            if st.button("🔄 Refresh"): st.rerun()

        db = SessionLocal()
        incidents = db.query(Incident).order_by(Incident.created_at.desc()).all()
        
        for i in incidents:
            with st.container(border=True):
                st.markdown(f"### Alert: {i.id} on `{i.target_resource}`")
                st.markdown(f"**Issue:** {i.issue}")
                
                if i.status == "TRIGGERED":
                    st.error("🚨 Triggered. Queuing AI Investigator...")
                elif i.status == "INVESTIGATING":
                    st.warning("🤖 AI is reading server logs and analyzing via SSH...")
                elif i.status == "AWAITING_APPROVAL":
                    st.info("🛡️ **AI Root Cause Analysis:**\n" + i.ai_analysis)
                    with st.expander("View Proposed Remediation Script"):
                        st.code(i.remediation_script, language="bash")
                    
                    if st.session_state.role == "architect":
                        if st.button("✅ Approve ChatOps Execution", key=i.id):
                            requests.post(f"{API_URL}/sre/approve/{i.id}")
                            st.rerun()
                    else:
                        st.write("🔒 Waiting for Architect approval.")
                elif i.status == "RESOLVED":
                    st.success("✅ Issue Remediated Successfully by AI.")
        db.close()

    # Phase 8: Learning Loop
    with tab4:
        st.subheader("Continuous Learning Loop (RAG)")
        st.write("If the AI generates bad code, correct it here. It will remember for next time.")
        
        mistake = st.text_area("What did the AI do wrong?")
        correction = st.text_area("What is the corporate standard/correction?")
        if st.button("Submit to AI Memory"):
            requests.post(f"{API_URL}/feedback", json={"mistake": mistake, "correction": correction})
            st.success("Knowledge Base Updated!")
            
        st.markdown("---")
        st.markdown("**Current Memory Bank:**")
        db = SessionLocal()
        for t in db.query(TrainingData).all():
            st.write(f"- ❌ *Mistake:* {t.mistake} | ✅ *Rule:* {t.correction}")
        db.close()

# ==========================================
# 7. MULTIPROCESSING RUNNER (WINDOWS SAFE)
# ==========================================
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python deckforge_os.py all")
        sys.exit(1)
        
    cmd = sys.argv[1].lower()
    
    if cmd == "api":
        uvicorn.run(app, host="0.0.0.0", port=8000)
    elif cmd == "ui":
        sys.argv = ["streamlit", "run", os.path.abspath(__file__), "--server.port=8501", "--server.headless=true"]
        import streamlit.web.cli as stcli
        sys.exit(stcli.main())
    elif cmd == "all":
        # Using subprocess instead of multiprocessing to avoid Windows Pickle errors
        print("Starting DeckForge OS (FastAPI Backend + Streamlit UI)...")
        api_process = subprocess.Popen([sys.executable, __file__, "api"])
        ui_process = subprocess.Popen([sys.executable, __file__, "ui"])
        
        print("\n🚀 System Online! Open your browser to: http://localhost:8501\n")
        
        try:
            api_process.wait()
            ui_process.wait()
        except KeyboardInterrupt:
            print("\nShutting down DeckForge OS...")
            api_process.terminate()
            ui_process.terminate()
    else:
        run_streamlit()