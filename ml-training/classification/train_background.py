"""
Background training script with progress logging
Runs training with periodic status updates to a log file
"""

import sys
import subprocess
import time
from pathlib import Path

# Setup paths
classification_dir = Path(__file__).parent
log_file = classification_dir / "training_progress.log"

def run_training():
    """Run training in background with output logging"""
    
    print("=" * 70)
    print("STARTING BACKGROUND TRAINING")
    print("=" * 70)
    print(f"Log file: {log_file}")
    print(f"Monitor progress: Get-Content {log_file} -Wait")
    print("=" * 70)
    
    # Open log file
    with open(log_file, 'w', encoding='utf-8') as f:
        f.write("=" * 70 + "\n")
        f.write(f"Training started at: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("=" * 70 + "\n\n")
        f.flush()
        
        # Run training with output to log
        process = subprocess.Popen(
            [sys.executable, "train.py"],
            cwd=classification_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
            universal_newlines=True
        )
        
        # Stream output to both console and log
        for line in process.stdout:
            print(line, end='')
            f.write(line)
            f.flush()
        
        # Wait for completion
        process.wait()
        
        # Write completion status
        f.write("\n" + "=" * 70 + "\n")
        f.write(f"Training finished at: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Exit code: {process.returncode}\n")
        f.write("=" * 70 + "\n")
    
    print("\n" + "=" * 70)
    print("TRAINING COMPLETE")
    print(f"Exit code: {process.returncode}")
    print("=" * 70)
    
    return process.returncode

if __name__ == "__main__":
    exit_code = run_training()
    sys.exit(exit_code)
