#!/usr/bin/env python3
"""
Dependency installer for BUBT Lost and Found System
This script will try to install pip and required packages
"""

import subprocess
import sys
import os

def run_command(cmd, check=True):
    """Run a shell command"""
    try:
        result = subprocess.run(cmd, shell=True, check=check, 
                              capture_output=True, text=True)
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def check_pip():
    """Check if pip is installed"""
    success, _, _ = run_command("python3 -m pip --version", check=False)
    return success

def install_pip():
    """Try to install pip"""
    print("🔧 Attempting to install pip...")
    
    # Try ensurepip first
    print("   Trying ensurepip...")
    success, out, err = run_command("python3 -m ensurepip --upgrade", check=False)
    if success:
        print("   ✅ pip installed using ensurepip")
        return True
    
    # Try apt-get
    print("   Trying apt-get...")
    success, out, err = run_command("sudo apt update && sudo apt install -y python3-pip", check=False)
    if success:
        print("   ✅ pip installed using apt-get")
        return True
    
    print("   ❌ Could not install pip automatically")
    print("   Please install pip manually:")
    print("      sudo apt update")
    print("      sudo apt install python3-pip -y")
    return False

def install_requirements():
    """Install required packages"""
    print("\n📦 Installing required packages...")
    
    packages = ['Flask==2.3.3', 'Flask-SQLAlchemy==3.0.5', 'Werkzeug==2.3.7']
    
    for package in packages:
        print(f"   Installing {package}...")
        success, out, err = run_command(f"python3 -m pip install {package}", check=False)
        if success:
            print(f"   ✅ {package} installed")
        else:
            print(f"   ❌ Failed to install {package}")
            print(f"   Error: {err}")
            return False
    
    return True

def main():
    print("=" * 50)
    print("BUBT Lost and Found System - Dependency Installer")
    print("=" * 50)
    print()
    
    # Check if pip is installed
    if not check_pip():
        print("❌ pip is not installed")
        if not install_pip():
            sys.exit(1)
    else:
        print("✅ pip is already installed")
    
    # Install requirements
    if not install_requirements():
        print("\n❌ Failed to install some packages")
        sys.exit(1)
    
    print("\n✅ All dependencies installed successfully!")
    print("\n🚀 You can now run the application:")
    print("   python3 app.py")
    print("   or")
    print("   ./run.sh")

if __name__ == "__main__":
    main()

