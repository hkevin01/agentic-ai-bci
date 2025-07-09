#!/usr/bin/env python3
"""
Development setup script for the Agentic AI BCI Research Assistant.
"""

import subprocess
import sys
from pathlib import Path

from loguru import logger


def run_command(
    command: str, check: bool = True
) -> subprocess.CompletedProcess:
    """Run a shell command and return the result."""
    logger.info(f"Running: {command}")
    result = subprocess.run(
        command, shell=True, capture_output=True, text=True, check=check
    )
    if result.stdout:
        logger.info(result.stdout.strip())
    if result.stderr and result.returncode != 0:
        logger.error(result.stderr.strip())
    return result


def setup_development_environment():
    """Set up the development environment."""
    logger.info("Setting up development environment...")
    
    # Create virtual environment if it doesn't exist
    venv_path = Path("venv")
    if not venv_path.exists():
        logger.info("Creating virtual environment...")
        run_command(f"{sys.executable} -m venv venv")
    
    # Install dependencies
    pip_cmd = "venv/bin/pip" if sys.platform != "win32" else "venv\\Scripts\\pip"
    
    logger.info("Installing dependencies...")
    run_command(f"{pip_cmd} install --upgrade pip")
    run_command(f"{pip_cmd} install -r requirements.txt")
    
    # Install pre-commit hooks
    logger.info("Setting up pre-commit hooks...")
    run_command(f"{pip_cmd} install pre-commit")
    run_command("venv/bin/pre-commit install" if sys.platform != "win32" 
                else "venv\\Scripts\\pre-commit install")


def setup_directories():
    """Create necessary project directories."""
    directories = [
        "src/agents",
        "src/models",
        "src/services",
        "src/ui",
        "src/api",
        "src/utils",
        "tests/unit",
        "tests/integration",
        "tests/fixtures",
        "data/raw",
        "data/processed",
        "data/external",
        "logs",
        "models/saved",
        "models/checkpoints",
        "uploads",
        "config",
        "notebooks"
    ]
    
    logger.info("Creating project directories...")
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        # Create __init__.py files for Python packages
        if directory.startswith("src/") or directory.startswith("tests/"):
            init_file = Path(directory) / "__init__.py"
            if not init_file.exists():
                init_file.touch()


def create_pre_commit_config():
    """Create pre-commit configuration."""
    config_content = """repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.4.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files
      - id: check-merge-conflict
  
  - repo: https://github.com/psf/black
    rev: 23.9.1
    hooks:
      - id: black
        language_version: python3
  
  - repo: https://github.com/pycqa/flake8
    rev: 6.1.0
    hooks:
      - id: flake8
        args: [--max-line-length=88, --extend-ignore=E203,W503]
  
  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.6.1
    hooks:
      - id: mypy
        additional_dependencies: [types-requests, types-PyYAML]
        args: [--ignore-missing-imports]
"""
    
    with open(".pre-commit-config.yaml", "w") as f:
        f.write(config_content)
    logger.info("Created pre-commit configuration")


def main():
    """Main setup function."""
    logger.info("Starting development environment setup...")
    
    try:
        setup_directories()
        create_pre_commit_config()
        setup_development_environment()
        
        logger.info("✅ Development environment setup complete!")
        logger.info("Next steps:")
        logger.info("1. Copy .env.example to .env and fill in your API keys")
        logger.info("2. Run 'python scripts/run_app.py setup' to initialize data directories")
        logger.info("3. Run 'python scripts/run_app.py serve' to start the application")
        
    except Exception as e:
        logger.error(f"Setup failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
