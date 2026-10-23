================================================================================
                    SOUND MANAGER - BUILD GUIDE
================================================================================

QUICK START
-----------
To build the executable, simply run:

    build_exe.bat

That's it! The script will:
  1. Check for Python
  2. Install PyInstaller if needed
  3. Build SoundManager.exe
  4. Place it in the 'dist' folder

Output: dist\SoundManager.exe (~49 MB)

================================================================================

REQUIREMENTS
------------
- Windows 10/11
- Python 3.11 or higher
- Internet connection (for PyInstaller installation if needed)

The build script will automatically install PyInstaller if it's not found.

================================================================================

BUILD METHODS
-------------

METHOD 1: Batch File (Easiest)
-------------------------------
Double-click:  build_exe.bat

This is the recommended method for most users.


METHOD 2: Python Script
------------------------
Run in terminal:  python build_exe.py

Options:
  python build_exe.py          # Full clean build
  python build_exe.py --quick  # Quick rebuild
  python build_exe.py --help   # Show help


METHOD 3: Quick Rebuild
------------------------
After first build, use:  REBUILD.bat

This is faster for subsequent builds.


METHOD 4: PyInstaller Direct
-----------------------------
For advanced users:  pyinstaller SoundManager.spec

================================================================================

WHAT GETS CREATED
-----------------

dist\
  SoundManager.exe ........... Main executable (DISTRIBUTE THIS)
  README.txt ................. User guide
  QUICK_REFERENCE.txt ........ Reference card

build\
  SoundManager\ .............. Build artifacts (can delete)

SoundManager.spec ............ Build configuration (keep for rebuilds)

================================================================================

TROUBLESHOOTING
---------------

Problem: "Python is not recognized"
Solution: Install Python from https://www.python.org/
          Make sure to check "Add Python to PATH" during installation

Problem: "PyInstaller not found"
Solution: Run: pip install pyinstaller
          Or let build_exe.bat install it automatically

Problem: "sound_manager_gui.py not found"
Solution: Make sure you're running the script from the Sound Manager directory
          Use: cd "D:\Projects\Sound Manager"

Problem: Build succeeds but .exe doesn't run
Solution: 1. Check antivirus (may be blocking)
          2. Add dist folder to antivirus exclusions
          3. Run from command line to see errors

Problem: Windows SmartScreen warning
Solution: This is normal for unsigned executables
          Click "More info" → "Run anyway"

================================================================================

AFTER BUILDING
--------------

1. Test the executable:
   - Run dist\SoundManager.exe
   - Verify all features work
   - Check icon appears correctly

2. Distribute to colleagues:
   - Share dist\SoundManager.exe
   - Include dist\README.txt
   - No other files needed!

3. Recipients need:
   - Windows 10 or 11 (64-bit)
   - Nothing else! No Python, no libraries, nothing.

================================================================================

REBUILDING AFTER CHANGES
-------------------------

If you modify the code:

1. Edit sound_manager_gui.py
2. Save changes
3. Run: REBUILD.bat
4. Test: dist\SoundManager.exe

The rebuild is faster than the initial build.

================================================================================

FILE SIZES
----------

Source code:          ~30 KB   (sound_manager_gui.py)
Icon:                 ~50 KB   (sound_manager_icon.ico)
Executable:           ~49 MB   (SoundManager.exe)

Why is the .exe so large?
  - Includes Python interpreter (~15 MB)
  - Includes PyQt6 framework (~25 MB)
  - Includes all dependencies (~9 MB)
  - Everything needed to run!

================================================================================

DISTRIBUTION
------------

What to share:
  MINIMUM:  SoundManager.exe
  BETTER:   SoundManager.exe + README.txt
  BEST:     SoundManager.exe + README.txt + QUICK_REFERENCE.txt

How to share:
  - Email (compress to zip if size is an issue)
  - Network share
  - USB drive
  - Cloud storage (OneDrive, Google Drive, etc.)

Recipients just:
  1. Download/copy SoundManager.exe
  2. Double-click to run
  3. Done!

================================================================================

BUILD SCRIPTS SUMMARY
---------------------

build_exe.bat ........... Full clean build with checks (RECOMMENDED)
REBUILD.bat ............. Quick rebuild using spec file
build_exe.py ............ Python build script with options
SoundManager.spec ....... PyInstaller configuration

Use build_exe.bat for first build or major changes.
Use REBUILD.bat for quick rebuilds after minor changes.

================================================================================

TIPS
----

✓ Always test the .exe before distributing
✓ Keep SoundManager.spec for faster rebuilds
✓ Delete build\ folder to save disk space
✓ Compress .exe to zip for easier emailing
✓ Include README.txt when sharing

================================================================================

NEED MORE HELP?
---------------

See detailed documentation:
  - BUILD_INSTRUCTIONS.md .... Complete build guide
  - DISTRIBUTION_GUIDE.md .... How to share with colleagues
  - product presentation\ .... Full user documentation

================================================================================

QUICK COMMAND REFERENCE
-----------------------

Build executable:         build_exe.bat
Quick rebuild:            REBUILD.bat
Test executable:          dist\SoundManager.exe
Install PyInstaller:      pip install pyinstaller
Check Python version:     python --version

================================================================================

                        Happy Building!

================================================================================
