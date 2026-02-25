import os
from git import Repo
from github import Github

def delivery_node(state):
    if not state.git_config.enabled: return state
    token = os.getenv("GITHUB_TOKEN")
    path = f"exports/{state.current_blueprint.project_name}"
    
    # Git Init & Push logic
    try:
        g = Github(token)
        user = g.get_user()
        repo = user.create_repo(state.git_config.repo_name, private=True)
        # (Simplified for brevity: Real logic involves local git commit/push)
        state.deployment_url = repo.html_url
    except:
        pass
    return state