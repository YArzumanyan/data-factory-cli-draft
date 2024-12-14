import json
import os
from jsonschema import validate, ValidationError

# Load schemas at the module level
with open("schemas/pipeline_schema.json") as f:
    PIPELINE_SCHEMA = json.load(f)

with open("schemas/state_schema.json") as f:
    STATE_SCHEMA = json.load(f)

# Validate JSON against a schema
def validate_json(data, schema):
    try:
        validate(instance=data, schema=schema)
    except ValidationError as e:
        raise ValueError(f"JSON validation error: {e.message}")

# Read a JSON file
def read_json(filepath):
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File not found: {filepath}")
    with open(filepath, "r") as f:
        return json.load(f)

# Write a JSON file
def write_json(filepath, data):
    with open(filepath, "w") as f:
        json.dump(data, f, indent=4)

# Read and validate pipeline JSON
def read_pipeline(filepath):
    data = read_json(filepath)
    validate_json(data, PIPELINE_SCHEMA)
    return data

# Read and validate state JSON
def read_state(filepath):
    data = read_json(filepath)
    validate_json(data, STATE_SCHEMA)
    return data
