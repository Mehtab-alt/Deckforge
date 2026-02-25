from langgraph.graph import StateGraph, END
from core.schema import AgentState, InfraBlueprint, ValidationResult
from agents.vision import vision_node
from agents.delivery import delivery_node
from core.llm_factory import get_llm
from core.memory import memory
from core.forge_engine import ForgeEngine
from core.validator import CodeValidator
import json, os

memory.initialize()

def context_node(state):
    return {"retrieved_policy": memory.retrieve(state.user_idea)}

def strategist_node(state):
    llm = get_llm(json_mode=True)
    res = llm.invoke(f"Return JSON for this infra idea: {state.user_idea}. Standards: {state.retrieved_policy}")
    data = json.loads(res.content)
    return {"current_blueprint": InfraBlueprint(**data)}

def forge_node(state):
    engine = ForgeEngine()
    return engine.render(state)

def validator_node(state):
    # Save files to disk for validator
    path = f"exports/{state.current_blueprint.project_name}"
    os.makedirs(path, exist_ok=True)
    for p, c in state.artifacts.items():
        fp = os.path.join(path, p)
        os.makedirs(os.path.dirname(fp), exist_ok=True)
        with open(fp, "w") as f: f.write(c)
    
    v = CodeValidator()
    status, err = v.validate_terraform(path)
    return {"validation_results": [ValidationResult(tool="Terraform", status=status, stderr=err)]}

workflow = StateGraph(AgentState)
workflow.add_node("vision", vision_node)
workflow.add_node("context", context_node)
workflow.add_node("strategist", strategist_node)
workflow.add_node("forge", forge_node)
workflow.add_node("validator", validator_node)
workflow.add_node("delivery", delivery_node)

workflow.set_entry_point("vision")
workflow.add_edge("vision", "context")
workflow.add_edge("context", "strategist")
workflow.add_edge("strategist", "forge")
workflow.add_edge("forge", "validator")
workflow.add_edge("validator", "delivery")
workflow.add_edge("delivery", END)

brain = workflow.compile()