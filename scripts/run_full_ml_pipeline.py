import subprocess
import sys
import os

def run_script(script_name):
    print(f"\n{'='*50}")
    print(f"RUNNING: {script_name}")
    print(f"{'='*50}\n")
    
    result = subprocess.run([sys.executable, script_name], capture_output=False)
    if result.returncode != 0:
        print(f"\n[ERROR] {script_name} failed with exit code {result.returncode}. Aborting pipeline.")
        sys.exit(result.returncode)
    else:
        print(f"\n[SUCCESS] {script_name} completed successfully.")

def main():
    print("Starting Full ML Pipeline Rebuild...\n")
    
    scripts = [
        'run_preprocessing.py',
        'run_fe.py',
        'run_training.py'
    ]
    
    for script in scripts:
        if not os.path.exists(script):
            print(f"[ERROR] Script not found: {script}")
            sys.exit(1)
        run_script(script)
        
    print("\n" + "="*50)
    print("FULL ML PIPELINE COMPLETED SUCCESSFULLY")
    print("==================================================")
    print("Check models/ and logs/ for the generated outputs.")

if __name__ == "__main__":
    main()
