import os
import uuid
from utils.file_operations import read_pipeline, write_json
from models.state import PipelineState

DATA_FACTORY_HOME = os.getenv("DATA_FACTORY_HOME", os.path.expanduser("~/data-factory-home"))
PIPELINES_DIR = os.path.join(DATA_FACTORY_HOME, "pipelines")

# Ensure the storage directory exists
os.makedirs(PIPELINES_DIR, exist_ok=True)

def create_pipeline(user_file: str):
    # Read and validate user pipeline file
    pipeline = read_pipeline(user_file)
    
    # Assign a unique ID if not already present
    if "id" not in pipeline:
        pipeline["id"] = uuid.uuid4()
    
    # Determine file paths
    pipeline_id = pipeline["id"]
    version = 1
    pipeline_file = os.path.join(PIPELINES_DIR, f"{pipeline_id}_{version}.json")
    state_file = os.path.join(PIPELINES_DIR, f"{pipeline_id}_state.json")
    
    # Save the pipeline file
    write_json(pipeline_file, pipeline)
    
    # Create or update the state file
    state = PipelineState(latest_version=version, versions={version: os.path.basename(pipeline_file)})
    write_json(state_file, state.to_dict())
    
    # Update the user file to include the pipeline ID
    write_json(user_file, pipeline)
    
    print(f"Pipeline created with ID: {pipeline_id}")

def update_pipeline(user_file: str):
    # Read and validate user pipeline file
    pipeline = read_pipeline(user_file)
    
    # Ensure the pipeline has an ID
    if "id" not in pipeline:
        raise ValueError("Pipeline must have an ID. Use 'create' command first.")
    
    # Determine file paths
    pipeline_id = pipeline["id"]
    state_file = os.path.join(PIPELINES_DIR, f"{pipeline_id}_state.json")
    
    # Load the state file
    state_data = read_pipeline(state_file)
    state = PipelineState.from_dict(state_data)
    
    # Increment the version number
    new_version = state.latest_version + 1
    pipeline_file = os.path.join(PIPELINES_DIR, f"{pipeline_id}_{new_version}.json")
    
    # Save the new version
    write_json(pipeline_file, pipeline)
    
    # Update the state file
    state.latest_version = new_version
    state.versions[new_version] = os.path.basename(pipeline_file)
    write_json(state_file, state.to_dict())
    
    print(f"Pipeline updated to version {new_version}")
