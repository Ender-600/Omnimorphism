import subprocess
from datetime import datetime

def git_commit(filename, class_name, method_name):
    branch_name = f"auto-gen/{class_name}_{method_name}_{datetime.now().strftime('%Y%m%d%H%M%S')}"
    subprocess.run(["git", "checkout", "-b", branch_name])
    subprocess.run(["git", "add", filename])
    commit_message = f"Auto-generated {method_name}() for {class_name} on {datetime.now().isoformat()}"
    subprocess.run(["git", "commit", "-m", commit_message])
