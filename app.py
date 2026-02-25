import streamlit as st
import base64, uuid
from core.schema import AgentState, GitConfig, LiveResource
from agents.orchestrator import brain
from core.state_parser import StateParser

st.set_page_config(layout="wide", page_title="DeckForge")
st.title("⚒️ DeckForge: Phases 1-5")

if "id" not in st.session_state: st.session_state.id = str(uuid.uuid4())

with st.sidebar:
    st.header("Project Delivery")
    do_git = st.checkbox("Push to GitHub")
    repo_name = st.text_input("Repo Name", "my-infra-project")

col1, col2 = st.columns([2,1])
with col1:
    idea = st.text_area("Describe the project...", height=150)
with col2:
    file = st.file_uploader("Upload Diagram", type=['png','jpg'])

if st.button("Forge Infrastructure"):
    img_b64 = base64.b64encode(file.getvalue()).decode() if file else None
    state = AgentState(
        thread_id=st.session_state.id,
        user_idea=idea,
        image_data=img_b64,
        git_config=GitConfig(enabled=do_git, repo_name=repo_name)
    )
    
    with st.status("Agents forging...") as s:
        final = brain.invoke(state)
        st.session_state.final = final
        s.update(label="Forge Complete", state="complete")

if "final" in st.session_state:
    res = st.session_state.final
    t1, t2, t3, t4 = st.tabs(["🏗️ Strategy", "💻 Code", "🛡️ Validation", "🛰️ Live State"])
    
    with t1:
        st.json(res['current_blueprint'].model_dump())
        st.info(f"Policy Context: {res['retrieved_policy']}")
    with t2:
        for p, c in res['artifacts'].items():
            with st.expander(p): st.code(c)
    with t3:
        for v in res['validation_results']:
            st.write(f"**{v.tool}**: {v.status}")
            if v.stderr: st.error(v.stderr)
    with t4:
        # Phase 5: Simulated State Parsing
        parser = StateParser()
        live = parser.parse_state(f"exports/{res['current_blueprint'].project_name}")
        st.table(live)