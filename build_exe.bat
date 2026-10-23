@echo off
cls
echo ====================================================================
echo           SOUND MANAGER - EXECUTABLE BUILDER
echo ====================================================================
echo.
echo This script will create a standalone SoundManager.exe file.
echo.
echo Requirements:
echo   - Python 3.x installed
echo   - PyInstaller package
echo.
echo The build process will:
echo   1. Check for PyInstaller (install if missing)
echo   2. Clean previous builds
echo   3. Create standalone .exe with embedded icon
echo   4. Package everything into one file
echo.
echo Output: dist\SoundManager.exe (~49 MB)
echo.
echo ====================================================================
pause
echo.

REM Check if Python is available
echo [1/5] Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH!
    echo Please install Python from https://www.python.org/
    echo.
    pause
    exit /b 1
)
python --version
echo OK - Python found!
echo.

REM Check if source file exists
echo [2/5] Checking source files...
if not exist "sound_manager_gui.py" (
    echo ERROR: sound_manager_gui.py not found!
    echo Please run this script from the Sound Manager directory.
    echo.
    pause
    exit /b 1
)
if not exist "sound_manager_icon.ico" (
    echo WARNING: sound_manager_icon.ico not found!
    echo The executable will be created without an icon.
    echo.
)
echo OK - Source files found!
echo.

REM Check/Install PyInstaller
echo [3/5] Checking PyInstaller...
python -c "import PyInstaller" >nul 2>&1
if errorlevel 1 (
    echo PyInstaller not found. Installing...
    python -m pip install pyinstaller
    if errorlevel 1 (
        echo ERROR: Failed to install PyInstaller!
        echo.
        pause
        exit /b 1
    )
    echo OK - PyInstaller installed!
) else (
    echo OK - PyInstaller already installed!
)
echo.

REM Build the executable
echo [4/5] Building executable...
echo This may take 1-2 minutes. Please wait...
echo.

pyinstaller --name=SoundManager --onefile --windowed --icon=sound_manager_icon.ico --add-data="sound_manager_icon.ico;." --noconsole --clean sound_manager_gui.py

if errorlevel 1 (
    echo.
    echo ====================================================================
    echo ERROR: Build failed!
    echo ====================================================================
    echo.
    echo Please check the error messages above.
    echo.
    pause
    exit /b 1
)

echo.
echo [5/5] Verifying output...
if exist "dist\SoundManager.exe" (
    echo OK - Executable created successfully!
    echo.
    echo ====================================================================
    echo                    BUILD SUCCESSFUL!
    echo ====================================================================
    echo.
    echo Executable location: dist\SoundManager.exe
    echo.
    
    REM Get file size
    for %%A in ("dist\SoundManager.exe") do (
        set size=%%~zA
        set /a sizeMB=%%~zA/1048576
    )
    echo File size: ~!sizeMB! MB
    echo.
    echo This is a STANDALONE executable:
    echo   - No Python required
    echo   - No additional files needed
    echo   - Ready to share with colleagues
    echo.
    echo Distribution files:
    echo   - dist\SoundManager.exe (main executable)
    echo   - dist\README.txt (user guide)
    echo   - dist\QUICK_REFERENCE.txt (reference card)
    echo.
    echo ====================================================================
    echo.
    echo Build artifacts (can be deleted):
    echo   - build\ folder
    echo   - SoundManager.spec file
    echo.
    echo To rebuild in the future, just run this batch file again!
    echo.
) else (
    echo ERROR: Executable not found in dist folder!
    echo Build may have failed silently.
    echo.
)

pause
