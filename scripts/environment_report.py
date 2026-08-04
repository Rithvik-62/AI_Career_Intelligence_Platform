import os
import sys
import platform
import importlib
import subprocess

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.diagnostics import run_all_diagnostics

def print_result(name, result):
    status = result.get('status', 'FAIL')
    msg = result.get('message', '')
    
    if status == 'PASS':
        print(f"[\033[92mPASS\033[0m] {name}: {msg}")
    elif status == 'WARNING':
        print(f"[\033[93mWARNING\033[0m] {name}: {msg}")
        if 'fix' in result:
            print(f"    -> Suggested Fix: {result['fix']}")
    else:
        print(f"[\033[91mFAIL\033[0m] {name}: {msg}")
        if 'details' in result:
            for detail in result['details']:
                print(f"    - {detail}")
        if 'fix' in result:
            print(f"    -> Suggested Fix: {result['fix']}")

def main():
    print("="*60)
    print("AI Career Intelligence Platform - Environment Report")
    print("="*60)
    
    # OS info
    print(f"Operating System: {platform.system()} {platform.release()} ({platform.version()})")
    
    # Virtual Environment
    is_venv = hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix)
    if is_venv:
        print_result("Virtual Environment", {"status": "PASS", "message": f"Active ({sys.prefix})"})
    else:
        print_result("Virtual Environment", {"status": "WARNING", "message": "Not running in a virtual environment.", "fix": "python -m venv .venv && source .venv/bin/activate"})
        
    print("-" * 60)
    
    diagnostics = run_all_diagnostics()
    results = diagnostics['results']
    
    print_result("Python Version", results['python'])
    print_result("Folder Permissions", results['directories'])
    print_result("Required Packages", results['packages'])
    print_result("NLTK Resources", results['nltk'])
    print_result("Machine Learning Models", results['models'])
    print_result("Datasets", results['datasets'])
    
    print("="*60)
    overall = diagnostics['overall_status']
    if overall == 'PASS':
        print(f"OVERALL STATUS: [\033[92mPASS\033[0m] Environment is ready.")
    elif overall == 'WARNING':
        print(f"OVERALL STATUS: [\033[93mWARNING\033[0m] Environment has warnings, but application can run.")
    else:
        print(f"OVERALL STATUS: [\033[91mFAIL\033[0m] Environment is not ready. Please fix the above errors.")
    print("="*60)

if __name__ == "__main__":
    main()
