import os
from utils.file_operations import read_pipeline, write_json

def generate_pipeline(user_file: str, output_script: str = "run_pipeline.py"):
    """
    Generate a Python script to run the pipeline in a Docker container.
    """
    # Read and validate the pipeline
    pipeline = read_pipeline(user_file)
    
    # Extract pipeline nodes and edges
    nodes = pipeline["nodes"]
    edges = pipeline["edges"]

    # Create the Python script content
    script_lines = [
        "import os",
        "import subprocess",
        "",
        "# Docker container setup",
        "CONTAINER_NAME = 'pipeline-container'",
        "DOCKER_IMAGE = 'python:3.9-slim'",
        "",
        "def setup_container():",
        "    subprocess.run(['docker', 'pull', DOCKER_IMAGE], check=True)",
        "    subprocess.run(['docker', 'run', '--name', CONTAINER_NAME, '-d', DOCKER_IMAGE, 'tail', '-f', '/dev/null'], check=True)",
        "",
        "def teardown_container():",
        "    subprocess.run(['docker', 'stop', CONTAINER_NAME], check=True)",
        "    subprocess.run(['docker', 'rm', CONTAINER_NAME], check=True)",
        "",
        "def copy_to_container(local_path, container_path):",
        "    subprocess.run(['docker', 'cp', local_path, f'{CONTAINER_NAME}:{container_path}'], check=True)",
        "",
        "def run_script_in_container(script_path, args):",
        "    cmd = ['docker', 'exec', CONTAINER_NAME, 'python', script_path] + args",
        "    subprocess.run(cmd, check=True)",
        "",
        "def main():",
        "    try:",
        "        setup_container()",
        ""
    ]

    # Add copy and execution steps
    for node in nodes:
        if node["type"] == "script":
            if "path" in node:
                # Local script
                script_path = node["path"]
                container_script_path = f"/app/{os.path.basename(script_path)}"
                script_lines.append(f"        copy_to_container('{script_path}', '{container_script_path}')")
                script_lines.append(f"        run_script_in_container('{container_script_path}', [])")
            else:
                # Catalog-based script
                script_lines.append(f"        print('TODO: Download script with ID {node['script_id']} into container')")
        
        elif node["type"] == "dataset":
            if "path" in node:
                # Local dataset
                dataset_path = node["path"]
                container_dataset_path = f"/data/{os.path.basename(dataset_path)}"
                script_lines.append(f"        copy_to_container('{dataset_path}', '{container_dataset_path}')")
            else:
                # Catalog-based dataset
                script_lines.append(f"        print('TODO: Download dataset with ID {node['dataset_id']} into container')")

    script_lines.append("")
    script_lines.append("    finally:")
    script_lines.append("        teardown_container()")
    script_lines.append("")
    script_lines.append("if __name__ == '__main__':")
    script_lines.append("    main()")

    # Write the Python script to the output file
    with open(output_script, "w") as f:
        f.write("\n".join(script_lines))
    
    print(f"Pipeline execution script generated: {output_script}")
