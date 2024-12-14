import os
from utils.file_operations import read_state

DATA_FACTORY_HOME = os.getenv("DATA_FACTORY_HOME", os.path.expanduser("~/data-factory-home"))
PIPELINES_DIR = os.path.join(DATA_FACTORY_HOME, "pipelines")

def list_pipelines():
    """List all pipelines stored locally."""
    if not os.path.exists(PIPELINES_DIR):
        print("No pipelines directory found. Try creating a pipeline first.")
        return
    
    state_files = [f for f in os.listdir(PIPELINES_DIR) if f.endswith("_state.json")]
    
    if not state_files:
        print("No pipelines found.")
        return
    
    print("Available Pipelines:")
    for state_file in state_files:
        state_path = os.path.join(PIPELINES_DIR, state_file)
        state = read_state(state_path)
        pipeline_id = state_file.replace("_state.json", "")
        
        print(f"- Pipeline ID: {pipeline_id}")
        print(f"  Latest Version: {state['latest_version']}")
        print(f"  Versions:")
        for version, file in state["versions"].items():
            print(f"    - v{version}: {file}")
