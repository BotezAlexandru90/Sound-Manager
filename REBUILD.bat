@echo off
REM Quick rebuild script - uses existing spec file for faster builds

cls
echo ====================================================================
echo           SOUND MANAGER - QUICK REBUILD
echo ====================================================================
echo.
echo This script uses the existing SoundManager.spec file for faster builds.
echo Use build_exe.bat for a clean build from scratch.
echo.
pause
echo.

if not exist "SoundManager.spec" (
    echo ERROR: SoundManager.spec not found!
    echo Please run build_exe.bat first to create the spec file.
    echo.
    pause
    exit /b 1
)

echo Building from spec file...
echo.

pyinstaller SoundManager.spec

if errorlevel 1 (
    echo.
    echo ERROR: Build failed!
    echo.
    pause
    exit /b 1
)

echo.
echo ====================================================================
echo                    REBUILD SUCCESSFUL!
echo ====================================================================
echo.
echo Executable: dist\SoundManager.exe
echo.

if exist "dist\SoundManager.exe" (
    for %%A in ("dist\SoundManager.exe") do (
        set /a sizeMB=%%~zA/1048576
    )
    echo File size: ~!sizeMB! MB
)

echo.
pause
