"""
GAN-Sim-GAN PHASE 1 Master Script
Executes all dataset preparation steps in sequence
"""

import sys
import subprocess
from pathlib import Path


def print_header(title):
    """Print formatted section header"""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70 + "\n")


def run_script(script_name, description):
    """Run a Python script and handle errors"""
    print(f"▶️  {description}...")
    print(f"   Running: {script_name}\n")
    
    try:
        result = subprocess.run(
            [sys.executable, script_name],
            check=True,
            capture_output=False,
            text=True
        )
        print(f"\n✅ {description} completed successfully!")
        return True
    
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Error running {script_name}")
        print(f"   Exit code: {e.returncode}")
        print("\n⚠️  PHASE 1 stopped due to error.")
        print(f"   Please fix the issue and run 'python {script_name}' to continue.")
        return False
    
    except KeyboardInterrupt:
        print(f"\n\n⚠️  Script interrupted by user (Ctrl+C)")
        print(f"   You can resume by running: python {script_name}")
        return False


def check_prerequisites():
    """Check if all required scripts exist"""
    required_scripts = [
        'download_dataset.py',
        'inspect_dataset.py',
        'prepare_dataset.py',
        'dataset_report.py'
    ]
    
    missing = []
    for script in required_scripts:
        if not Path(script).exists():
            missing.append(script)
    
    if missing:
        print("❌ ERROR: Missing required scripts:")
        for script in missing:
            print(f"   - {script}")
        return False
    
    return True


def main():
    """Main execution function"""
    print_header("GAN-SIM-GAN: PHASE 1 - DATASET PREPARATION")
    
    print("This script will execute all PHASE 1 steps in sequence:")
    print("  1. Download dataset from Kaggle")
    print("  2. Inspect dataset structure and quality")
    print("  3. Create train/validation/test splits")
    print("  4. Generate visual reports")
    print("\n⏱️  Estimated time: 15-30 minutes (depends on internet speed)")
    print("\n💡 Note: You can also run each script individually if needed.")
    
    # Check prerequisites
    print("\n🔍 Checking prerequisites...")
    if not check_prerequisites():
        sys.exit(1)
    print("   ✓ All scripts found")
    
    # Confirm execution
    print("\n" + "-" * 70)
    response = input("\n▶️  Continue with PHASE 1 execution? (yes/no): ").strip().lower()
    
    if response not in ['yes', 'y']:
        print("\n⏸️  Execution cancelled.")
        print("   Run 'python run_phase1.py' when you're ready.")
        sys.exit(0)
    
    # Execute scripts in sequence
    scripts = [
        ('download_dataset.py', 'Step 1/4: Download Dataset'),
        ('inspect_dataset.py', 'Step 2/4: Inspect Dataset'),
        ('prepare_dataset.py', 'Step 3/4: Prepare Splits'),
        ('dataset_report.py', 'Step 4/4: Generate Reports')
    ]
    
    for i, (script, description) in enumerate(scripts, 1):
        print_header(description)
        
        success = run_script(script, description)
        
        if not success:
            print(f"\n⚠️  PHASE 1 incomplete. Stopped at step {i}/4.")
            print("\nTo resume:")
            for remaining_script, remaining_desc in scripts[i-1:]:
                print(f"   python {remaining_script}")
            sys.exit(1)
        
        # Small delay between scripts
        if i < len(scripts):
            print("\n" + "-" * 70)
            input("\n⏸️  Press Enter to continue to next step...")
    
    # Success!
    print_header("✅ PHASE 1 COMPLETED SUCCESSFULLY!")
    
    print("All dataset preparation steps completed!")
    print("\n📁 Generated outputs:")
    print("   • datasets/Apple/train/        - Training images")
    print("   • datasets/Apple/validation/   - Validation images")
    print("   • datasets/Apple/test/         - Test images")
    print("   • reports/*.json               - JSON reports")
    print("   • reports/*.png                - Visual charts")
    print("   • reports/*.txt                - Text summaries")
    
    print("\n🎯 Next steps:")
    print("   1. Review the generated reports in 'reports/' directory")
    print("   2. Check sample images to verify data quality")
    print("   3. Proceed to PHASE 2: Baseline Model Training")
    
    print("\n" + "=" * 70)
    print("Ready to train AI models! 🚀")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  PHASE 1 interrupted by user.")
        print("   You can resume by running individual scripts or 'python run_phase1.py'")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {str(e)}")
        print("   Please check the error message and try again.")
        sys.exit(1)
