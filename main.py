import typer
from commands.pipeline import create_pipeline, update_pipeline
from commands.list import list_pipelines
from commands.generate import generate_pipeline

app = typer.Typer()

@app.command()
def create(user_file: str):
    """Create a new pipeline."""
    create_pipeline(user_file)

@app.command()
def update(user_file: str):
    """Update an existing pipeline."""
    update_pipeline(user_file)

@app.command()
def list():
    """List all pipelines."""
    list_pipelines()

@app.command()
def generate(user_file: str, output_script: str = "run_pipeline.py"):
    """Generate a Python script to run the pipeline."""
    generate_pipeline(user_file, output_script)

if __name__ == "__main__":
    app()
