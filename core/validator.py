import subprocess, os, shutil

class CodeValidator:
    def validate_terraform(self, project_path):
        tf_path = os.path.join(project_path, "terraform")
        if not os.path.exists(tf_path): return "PASS", ""
        try:
            subprocess.run(["terraform", "init", "-backend=false"], cwd=tf_path, capture_output=True)
            res = subprocess.run(["terraform", "validate"], cwd=tf_path, capture_output=True, text=True)
            return ("PASS", "") if res.returncode == 0 else ("FAIL", res.stderr)
        except Exception as e:
            return "FAIL", str(e)