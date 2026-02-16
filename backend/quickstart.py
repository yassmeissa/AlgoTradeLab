#!/usr/bin/env python
"""
Quick start script for AlgoTrade Lab Backend
Run: python quickstart.py
"""

import os
import sys
import subprocess
from pathlib import Path


def run_command(command, description):
    """Run a command and report status"""
    print(f"\n{'='*50}")
    print(f"➜ {description}")
    print(f"{'='*50}")
    result = subprocess.run(command, shell=True)
    if result.returncode != 0:
        print(f"✗ Failed: {description}")
        return False
    print(f"✓ Done: {description}")
    return True


def main():
    """Main quickstart routine"""
    print("""
    ╔══════════════════════════════════════════════════╗
    ║     AlgoTrade Lab Backend - Quick Start          ║
    ╚══════════════════════════════════════════════════╝
    """)
    
    # Check Python version
    print(f"✓ Python {sys.version.split()[0]}")
    
    # Create venv
    if not Path("venv").exists():
        if not run_command("python -m venv venv", "Creating virtual environment"):
            return
    
    # Determine activation command
    activate_cmd = "source venv/bin/activate" if sys.platform != "win32" else "venv\\Scripts\\activate"
    
    # Install requirements
    if not run_command(f"{activate_cmd} && pip install -r requirements.txt", 
                       "Installing dependencies"):
        return
    
    # Create .env if needed
    if not Path(".env").exists():
        print("\n✓ Creating .env file...")
        if Path(".env.example").exists():
            with open(".env.example") as f:
                content = f.read()
            with open(".env", "w") as f:
                f.write(content)
            print("  ⚠️  Edit .env with your configuration")
    
    # Display next steps
    print(f"""
    ╔══════════════════════════════════════════════════╗
    ║           Setup Completed Successfully!          ║
    ╚══════════════════════════════════════════════════╝
    
    Next steps:
    
    1. Activate virtual environment:
       {activate_cmd}
    
    2. Start PostgreSQL and Redis (using Docker):
       docker-compose up -d
    
    3. Run the server:
       python run.py
    
    4. Access API documentation:
       http://localhost:8000/docs
    
    5. Run tests:
       pytest
    
    Happy trading! 📈
    """)


if __name__ == "__main__":
    main()
