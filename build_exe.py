"""
Build script for Sound Manager executable
Creates a standalone .exe file with all dependencies included

Usage:
    python build_exe.py              - Full clean build
    python build_exe.py --quick      - Quick rebuild using spec file
    python build_exe.py --help       - Show this help
"""
import os
import subprocess
import sys

def check_requirements():
    """Check if all required files exist"""
    print("Checking requirements...")
    
    required_files = [
        "sound_manager_gui.py",
        "sound_manager_icon.ico"
    ]
    
    missing = []
    for file in required_files:
        if os.path.exists(file):
            print(f"  ✓ {file}")
        else:
            print(f"  ✗ {file} - MISSING!")
            missing.append(file)
    
    if missing:
        print()
        print(f"ERROR: Missing required files: {', '.join(missing)}")
        return False
    
    print("✓ All required files found")
    return True

def install_pyinstaller():
    """Install PyInstaller if not available"""
    try:
        import PyInstaller
        print("✓ PyInstaller already installed")
        # Show version
        result = subprocess.run(
            ["pyinstaller", "--version"],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            print(f"  Version: {result.stdout.strip()}")
        return True
    except ImportError:
        print("✗ PyInstaller not found. Installing...")
        try:
            subprocess.check_call([
                sys.executable, "-m", "pip", "install", "pyinstaller"
            ])
            print("✓ PyInstaller installed successfully")
            return True
        except subprocess.CalledProcessError:
            print("✗ Failed to install PyInstaller")
            return False

def build_executable(quick=False):
    """Build standalone executable using PyInstaller"""
    
    print("=" * 70)
    print("Sound Manager - Executable Builder")
    print("=" * 70)
    print()
    
    # Check requirements
    if not quick and not check_requirements():
        return False
    
    print()
    
    # Check/Install PyInstaller
    if not install_pyinstaller():
        return False
    
    print()
    print("Building executable...")
    print("-" * 70)
    
    if quick and os.path.exists("SoundManager.spec"):
        # Quick rebuild using spec file
        print("Using existing SoundManager.spec for quick rebuild...")
        cmd = ["pyinstaller", "SoundManager.spec"]
    else:
        # Full build with all options
        print("Performing clean build...")
        cmd = [
            "pyinstaller",
            "--name=SoundManager",
            "--onefile",
            "--windowed",
            "--icon=sound_manager_icon.ico",
            "--add-data=sound_manager_icon.ico;.",
            "--noconsole",
            "--clean",
            "sound_manager_gui.py"
        ]
    
    print(f"Command: {' '.join(cmd)}")
    print()
    
    try:
        subprocess.check_call(cmd)
        print()
        print("=" * 70)
        print("✓ BUILD SUCCESSFUL!")
        print("=" * 70)
        print()
        
        exe_path = os.path.join("dist", "SoundManager.exe")
        if os.path.exists(exe_path):
            size_mb = os.path.getsize(exe_path) / (1024 * 1024)
            print(f"Executable: dist\\SoundManager.exe")
            print(f"File size:  {size_mb:.2f} MB")
            print()
            print("This is a STANDALONE executable:")
            print("  ✓ No Python required")
            print("  ✓ No additional files needed")
            print("  ✓ Ready to share with colleagues")
            print()
            print("Distribution files in 'dist' folder:")
            print("  - SoundManager.exe (main executable)")
            print("  - README.txt (user guide)")
            print("  - QUICK_REFERENCE.txt (reference card)")
            print()
            print("Build artifacts (can be deleted):")
            print("  - build\\ folder")
            print("  - SoundManager.spec file")
            print()
        else:
            print("WARNING: Executable not found at expected location!")
            return False
        
        return True
        
    except subprocess.CalledProcessError as e:
        print()
        print("=" * 70)
        print("✗ BUILD FAILED!")
        print("=" * 70)
        print(f"Error: {e}")
        print()
        print("Common issues:")
        print("  1. PyInstaller not installed: pip install pyinstaller")
        print("  2. Missing source files: check sound_manager_gui.py exists")
        print("  3. Icon file missing: check sound_manager_icon.ico exists")
        print()
        return False

def show_help():
    """Show help message"""
    print(__doc__)
    print()
    print("Examples:")
    print("  python build_exe.py              # Full clean build")
    print("  python build_exe.py --quick      # Quick rebuild")
    print("  python build_exe.py --help       # Show this help")
    print()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "--help" or sys.argv[1] == "-h":
            show_help()
            sys.exit(0)
        elif sys.argv[1] == "--quick" or sys.argv[1] == "-q":
            success = build_executable(quick=True)
        else:
            print(f"Unknown option: {sys.argv[1]}")
            show_help()
            sys.exit(1)
    else:
        success = build_executable(quick=False)
    
    sys.exit(0 if success else 1)
