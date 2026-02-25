from langchain_core.messages import HumanMessage
from core.llm_factory import get_llm

def vision_node(state):
    if not state.image_data: return {"user_idea": state.user_idea}
    llm = get_llm()
    msg = HumanMessage(content=[
        {"type": "text", "text": "Describe the architecture in this image."},
        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{state.image_data}"}}
    ])
    res = llm.invoke([msg])
    return {"user_idea": f"{state.user_idea}\nVisual Context: {res.content}"}