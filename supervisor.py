import subprocess
import time

def setup_test(scenario):
    # Writes either 'corrupt' or 'healthy' to status.txt
    with open("status.txt", "w") as f:
        f.write(scenario)

def supervisor():
    print("--- Initiating Self-Healing Supervisor ---")
    
    # Force a failure first to demonstrate self-healing
    setup_test("corrupt")
    
    while True:
        print("\n[SUPERVISOR] Running ML Pipeline...")
        try:
            subprocess.check_call(["python", "pipeline.py"])
            print("[SUPERVISOR] System is stable. Shutting down supervisor.")
            break 
            
        except subprocess.CalledProcessError:
            print("\n[HEALING ACTION] Anomaly detected! Pipeline crashed.")
            print("[HEALING ACTION] Diagnosing root cause... (Data Corruption found)")
            print("[HEALING ACTION] Applying fix: Switching to clean data backup...")
            
            # The Automated Recovery action
            setup_test("healthy") 
            
            print("[HEALING ACTION] Restarting pipeline in 3 seconds...\n")
            time.sleep(3)

if __name__ == "__main__":
    supervisor()