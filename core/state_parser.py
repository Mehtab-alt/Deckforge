import subprocess
import json
import os

class StateParser:
    def __init__(self, project_dir: str):
        self.wd = project_dir

    def get_live_resources(self):
        """Runs terraform show to get reality."""
        tf_dir = os.path.join(self.wd, "terraform")
        if not os.path.exists(os.path.join(tf_dir, ".terraform")):
            return [] # Not initialized

        try:
            # Security: Ensure we don't leak secrets to logs
            res = subprocess.run(
                ["terraform", "show", "-json"], 
                cwd=tf_dir, 
                capture_output=True, 
                text=True
            )
            if res.returncode != 0: return []
            
            state = json.loads(res.stdout)
            resources = []
            
            # Recursive parser for modules
            def extract(modules):
                for m in modules:
                    for r in m.get("resources", []):
                        resources.append({
                            "address": r.get("address"),
                            "type": r.get("type"),
                            "status": r.get("values", {}).get("instance_state", "unknown")
                        })
                    extract(m.get("child_modules", []))
            
            if "values" in state:
                extract([state["values"]["root_module"]])
                
            return resources
        except Exception:
            return []