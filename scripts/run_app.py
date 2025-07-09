#!/usr/bin/env python3
"""
Main application runner for the Agentic AI BCI Research Assistant.
This script provides a unified entry point for starting the application.
"""

import argparse
import asyncio
import subprocess
import sys
from pathlib import Path
from typing import Optional

import uvicorn
from loguru import logger

# Add src to Python path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))


def run_streamlit():
    """Run the Streamlit dashboard."""
    logger.info("Starting Streamlit dashboard...")
    subprocess.run([
        sys.executable, "-m", "streamlit", "run",
        str(Path(__file__).parent.parent / "src" / "ui" / "streamlit_app.py"),
        "--server.port", "8501",
        "--server.address", "0.0.0.0"
    ])


def run_fastapi(host: str = "0.0.0.0", port: int = 8000, reload: bool = False):
    """Run the FastAPI backend server."""
    logger.info(f"Starting FastAPI server on {host}:{port}")
    uvicorn.run(
        "src.api.main:app",
        host=host,
        port=port,
        reload=reload,
        log_level="info"
    )


def run_full_stack():
    """Run both FastAPI backend and Streamlit frontend."""
    import threading

    # Start FastAPI in a separate thread
    api_thread = threading.Thread(
        target=run_fastapi,
        kwargs={"host": "0.0.0.0", "port": 8000, "reload": False}
    )
    api_thread.daemon = True
    api_thread.start()
    
    # Give the API time to start
    import time
    time.sleep(3)
    
    # Start Streamlit in the main thread
    run_streamlit()


def setup_environment():
    """Set up the development environment."""
    logger.info("Setting up development environment...")
    
    # Create necessary directories
    directories = [
        "data/raw",
        "data/processed",
        "logs",
        "models/saved",
        "uploads"
    ]
    
    base_path = Path(__file__).parent.parent
    for directory in directories:
        (base_path / directory).mkdir(parents=True, exist_ok=True)
    
    logger.info("Environment setup complete!")


def main():
    """Main entry point for the application."""
    parser = argparse.ArgumentParser(
        description="Agentic AI BCI Research Assistant"
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # API server command
    api_parser = subparsers.add_parser("api", help="Run FastAPI backend server")
    api_parser.add_argument("--host", default="0.0.0.0", help="Host address")
    api_parser.add_argument("--port", type=int, default=8000, help="Port number")
    api_parser.add_argument("--reload", action="store_true", help="Enable auto-reload")
    
    # Streamlit dashboard command
    subparsers.add_parser("dashboard", help="Run Streamlit dashboard")
    
    # Full stack command
    subparsers.add_parser("serve", help="Run both API and dashboard")
    
    # Setup command
    subparsers.add_parser("setup", help="Set up development environment")
    
    args = parser.parse_args()
    
    if args.command == "api":
        run_fastapi(host=args.host, port=args.port, reload=args.reload)
    elif args.command == "dashboard":
        run_streamlit()
    elif args.command == "serve":
        run_full_stack()
    elif args.command == "setup":
        setup_environment()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
