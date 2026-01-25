#!/usr/bin/env python3
import argparse
import os
import subprocess
import sys
import re
from urllib.parse import urlparse

def get_repo_name(url):
    """Extracts the repository name from the URL."""
    path = urlparse(url).path
    # Handle trailing slash
    if path.endswith('/'):
        path = path[:-1]
    name = path.split('/')[-1]
    if name.endswith('.git'):
        name = name[:-4]
    return name

def sanitize_name(name):
    """Sanitizes the name to be a valid Python module name."""
    # Replace any character that is not alphanumeric or underscore with underscore
    name = re.sub(r'[^a-zA-Z0-9_]', '_', name)
    # Ensure it doesn't start with a number
    if name and name[0].isdigit():
        name = '_' + name
    return name

def main():
    # Check if running in a virtual environment
    if not (sys.prefix != sys.base_prefix or os.path.exists(os.path.join(sys.prefix, 'pyvenv.cfg'))):
        print("Error: This tool must be run within a virtual environment.")
        sys.exit(1)

    parser = argparse.ArgumentParser(description="Clone and run a service with gateway.py")
    parser.add_argument("url", help="GitHub URL of the repository")
    args = parser.parse_args()

    repo_name_raw = get_repo_name(args.url)
    module_name = sanitize_name(repo_name_raw)
    
    print(f"Preparing service: {module_name} from {args.url}")

    if args.url.startswith("ssh://") or args.url.startswith("https://"):
        # Clone or Pull
        if os.path.isdir(module_name):
            print(f"Directory '{module_name}' exists. Updating...")
            subprocess.check_call(['git', '-C', module_name, 'pull'])
        else:
            print(f"Cloning into '{module_name}'...")
            subprocess.check_call(['git', 'clone', args.url, module_name])

    if os.path.isdir(args.url):
        # Handle local directory case
        print(f"Using local directory '{args.url}'...")
        module_path = os.path.dirname(args.url)
        # Add the directory to sys.path so it can be imported
        sys.path.insert(0, module_path)

    # Install Dependencies
    print("Checking dependencies...")
    req_txt = os.path.join(module_name, 'requirements.txt')
    pyproject = os.path.join(module_name, 'pyproject.toml')
    setup_py = os.path.join(module_name, 'setup.py')

    pip_cmd = [sys.executable, '-m', 'pip', 'install']
    
    if os.path.exists(req_txt):
        print(f"Installing from {req_txt}...")
        subprocess.check_call(pip_cmd + ['-r', req_txt])
    elif os.path.exists(pyproject) or os.path.exists(setup_py):
        print("Installing package dependencies...")
        # Install the directory as a package (getting deps)
        subprocess.check_call(pip_cmd + [module_name])
    else:
        print("No dependency file found (requirements.txt, pyproject.toml, setup.py). Skipping installation.")

    # Run Gateway
    print("Starting gateway...")
    if not os.path.exists('gateway.py'):
        print("Error: gateway.py not found in current directory.")
        sys.exit(1)

    try:
        # Run gateway.py using the same interpreter
        subprocess.run([sys.executable, 'gateway.py'])
    except KeyboardInterrupt:
        print("\nGateway stopped.")

if __name__ == "__main__":
    main()
