from jinja2 import Environment, FileSystemLoader

class ForgeEngine:
    def __init__(self):
        self.env = Environment(loader=FileSystemLoader('templates'), trim_blocks=True)

    def render(self, state):
        bp = state.current_blueprint
        ctx = bp.model_dump()
        ctx['retrieved_policy'] = state.retrieved_policy
        
        manifest = {
            "terraform/main.tf": "terraform/main.tf.j2",
            "ansible/hardening.yml": "ansible/hardening.yml.j2",
            "README.md": "docs/README.md.j2"
        }
        if bp.app_config.enabled:
            manifest["docker/Dockerfile"] = "docker/Dockerfile.j2"
        
        for path, tmpl in manifest.items():
            state.artifacts[path] = self.env.get_template(tmpl).render(**ctx)
        
        state.diagram_code = f"graph TD; User-->VPC; subgraph VPC; App; DB; end"
        return state