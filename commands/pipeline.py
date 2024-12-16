import os
import uuid
from utils.file_operations import read_pipeline, read_state, write_json
from models.state import PipelineState

DATA_FACTORY_HOME = os.getenv("DATA_FACTORY_HOME", os.path.expanduser("~/data-factory-home"))
PIPELINES_DIR = os.path.join(DATA_FACTORY_HOME, "pipelines")

os.makedirs(PIPELINES_DIR, exist_ok=True)

def create_pipeline(user_file: str):
    pipeline = read_pipeline(user_file)
    
    if "id" in pipeline:
        print("To `create` a new pipeline the pipeline should not contain id.")
        return
        
    pipeline["id"] = uuid.uuid4().hex
    pipeline_id = pipeline["id"]
    version = 1
    pipeline_file = os.path.join(PIPELINES_DIR, f"{pipeline_id}_{version}.json")
    state_file = os.path.join(PIPELINES_DIR, f"{pipeline_id}_state.json")
    
    write_json(pipeline_file, pipeline)
    
    state = PipelineState(latest_version=version, versions={version: os.path.basename(pipeline_file)})
    write_json(state_file, state.to_dict())
    
    write_json(user_file, pipeline)
    
    print(f"Pipeline created with ID: {pipeline_id}")

def update_pipeline(user_file: str):
    pipeline = read_pipeline(user_file)
    
    if "id" not in pipeline:
        raise ValueError("Pipeline must have an ID. Use 'create' command first.")
    
    pipeline_id = pipeline["id"]
    state_file = os.path.join(PIPELINES_DIR, f"{pipeline_id}_state.json")
    
    state_data = read_state(state_file)
    state = PipelineState.from_dict(state_data)
    
    new_version = state.latest_version + 1
    pipeline_file = os.path.join(PIPELINES_DIR, f"{pipeline_id}_{new_version}.json")
    
    write_json(pipeline_file, pipeline)
    
    state.latest_version = new_version
    state.versions[new_version] = os.path.basename(pipeline_file)
    write_json(state_file, state.to_dict())
    
    print(f"Pipeline updated to version {new_version}")

def sync_pipeline(user_file: str):
    return

def share_pipeline():
    return