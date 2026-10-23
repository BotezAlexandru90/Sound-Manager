# 🔨 Build Instructions - Sound Manager

## 📋 Overview

This guide explains how to build the standalone `SoundManager.exe` executable from source code.

---

## ✅ Prerequisites

### Required

1. **Python 3.11+** installed and in PATH
   - Download from: https://www.python.org/
   - During installation, check "Add Python to PATH"

2. **Source files** in the same directory:
   - `sound_manager_gui.py` (main application)
   - `sound_manager_icon.ico` (application icon)

### Auto-Installed

- **PyInstaller** - Will be installed automatically if missing

---

## 🚀 Quick Start

### Method 1: Batch File (Recommended for Windows)

**Easiest method - just double-click!**

```batch
build_exe.bat
```

**What it does:**
1. ✅ Checks Python installation
2. ✅ Verifies source files exist
3. ✅ Installs PyInstaller if needed
4. ✅ Builds standalone executable
5. ✅ Shows file size and location

**Output:** `dist\SoundManager.exe`

---

### Method 2: Python Script

**More control and cross-platform**

```bash
# Full clean build
python build_exe.py

# Quick rebuild (uses existing spec file)
python build_exe.py --quick

# Show help
python build_exe.py --help
```

---

### Method 3: PyInstaller Directly

**For advanced users**

```bash
# Using spec file (fastest)
pyinstaller SoundManager.spec

# Manual command (full options)
pyinstaller --name=SoundManager --onefile --windowed --icon=sound_manager_icon.ico --add-data="sound_manager_icon.ico;." --noconsole --clean sound_manager_gui.py
```

---

## 📁 Build Scripts

### Available Scripts

| Script | Purpose | When to Use |
|--------|---------|-------------|
| **build_exe.bat** | Full clean build | First build or after major changes |
| **REBUILD.bat** | Quick rebuild | Minor code changes |
| **build_exe.py** | Python build script | Cross-platform or automation |

---

## 🔧 Detailed Instructions

### Step-by-Step: First Build

1. **Open Command Prompt or PowerShell**
   ```
   Press Win + R
   Type: cmd
   Press Enter
   ```

2. **Navigate to project directory**
   ```bash
   cd "D:\Projects\Sound Manager"
   ```

3. **Verify files exist**
   ```bash
   dir sound_manager_gui.py
   dir sound_manager_icon.ico
   ```

4. **Run build script**
   ```batch
   build_exe.bat
   ```

5. **Wait for completion** (1-2 minutes)

6. **Check output**
   ```
   Output: dist\SoundManager.exe (~49 MB)
   ```

---

### Step-by-Step: Rebuild After Changes

1. **Edit source code**
   - Modify `sound_manager_gui.py`
   - Save changes

2. **Quick rebuild**
   ```batch
   REBUILD.bat
   ```
   
   Or:
   ```bash
   python build_exe.py --quick
   ```

3. **Test the new executable**
   ```
   dist\SoundManager.exe
   ```

---

## 🎯 Build Options Explained

### PyInstaller Options

```bash
--name=SoundManager          # Output filename
--onefile                    # Single executable (not a folder)
--windowed                   # No console window (GUI app)
--icon=sound_manager_icon.ico # Embed application icon
--add-data="icon;."          # Include icon file in bundle
--noconsole                  # Hide console (same as --windowed)
--clean                      # Clean cache before build
```

### Why These Options?

- **`--onefile`**: Creates single .exe instead of folder with DLLs
- **`--windowed`**: Prevents black console window from appearing
- **`--icon`**: Embeds icon in executable (shows in taskbar/explorer)
- **`--add-data`**: Includes icon file for runtime use
- **`--clean`**: Ensures fresh build, removes old artifacts

---

## 📊 Build Output

### Files Created

```
D:\Projects\Sound Manager\
│
├── dist\
│   ├── SoundManager.exe ......... ⭐ Main executable (~49 MB)
│   ├── README.txt ............... User guide
│   └── QUICK_REFERENCE.txt ...... Reference card
│
├── build\
│   └── SoundManager\ ............ Build artifacts (can delete)
│
└── SoundManager.spec ............ Build configuration
```

### What to Keep

**Keep:**
- ✅ `dist\SoundManager.exe` - The executable
- ✅ `dist\README.txt` - User documentation
- ✅ `SoundManager.spec` - For quick rebuilds

**Can Delete:**
- ❌ `build\` folder - Temporary build files
- ❌ `__pycache__\` - Python cache

---

## 🐛 Troubleshooting

### Issue: "Python is not recognized"

**Problem:** Python not in PATH

**Solution:**
1. Reinstall Python
2. Check "Add Python to PATH" during installation
3. Or add manually to system PATH

---

### Issue: "PyInstaller not found"

**Problem:** PyInstaller not installed

**Solution:**
```bash
pip install pyinstaller
```

Or let the build script install it automatically.

---

### Issue: "sound_manager_gui.py not found"

**Problem:** Running script from wrong directory

**Solution:**
```bash
cd "D:\Projects\Sound Manager"
```

Make sure you're in the correct folder.

---

### Issue: "Icon file not found"

**Problem:** `sound_manager_icon.ico` missing

**Solution:**
1. Make sure icon file exists in project directory
2. Or remove `--icon` option from build command

**Note:** Build will succeed without icon, but .exe won't have custom icon.

---

### Issue: Build succeeds but .exe doesn't run

**Problem:** Missing dependencies or antivirus blocking

**Solutions:**
1. Check antivirus logs
2. Add `dist` folder to antivirus exclusions
3. Try running from command line to see error messages:
   ```bash
   cd dist
   SoundManager.exe
   ```

---

### Issue: "UPX is not available"

**Problem:** UPX compression tool not found (optional)

**Solution:**
- Ignore this warning - not critical
- Or install UPX from: https://upx.github.io/
- Or add `--noupx` to build command

---

### Issue: Build is very slow

**Problem:** First build includes dependency analysis

**Solutions:**
1. First build: 1-2 minutes (normal)
2. Subsequent builds: Use `REBUILD.bat` (faster)
3. Use `--quick` option: `python build_exe.py --quick`

---

## ⚡ Performance Tips

### Speed Up Builds

1. **Use spec file for rebuilds**
   ```bash
   pyinstaller SoundManager.spec
   ```
   Faster than full command.

2. **Don't use `--clean` every time**
   ```bash
   # Slower (clean build)
   pyinstaller --clean ...
   
   # Faster (incremental)
   pyinstaller SoundManager.spec
   ```

3. **Use quick rebuild script**
   ```batch
   REBUILD.bat
   ```

---

### Reduce File Size

Current size: ~49 MB

**Why so large?**
- Python interpreter: ~15 MB
- PyQt6 framework: ~25 MB
- Dependencies: ~9 MB

**Can't reduce much because:**
- All dependencies must be included
- PyQt6 is large but necessary
- Single-file executable includes everything

**Alternative (smaller but less convenient):**
- Use `--onedir` instead of `--onefile`
- Creates folder with .exe + DLLs
- Main .exe is smaller, but need whole folder

---

## 🔄 Build Workflow

### Development Cycle

```
1. Edit code
   ↓
2. Test with Python
   python sound_manager_gui.py
   ↓
3. Quick rebuild
   REBUILD.bat
   ↓
4. Test executable
   dist\SoundManager.exe
   ↓
5. Repeat as needed
```

### Release Cycle

```
1. Final code changes
   ↓
2. Update version number
   (in About dialog)
   ↓
3. Clean build
   build_exe.bat
   ↓
4. Test thoroughly
   ↓
5. Distribute
   Share dist\SoundManager.exe
```

---

## 📦 Distribution Preparation

### Before Sharing

1. **Clean build**
   ```batch
   build_exe.bat
   ```

2. **Test on your machine**
   - Launch executable
   - Test all features
   - Verify icon appears

3. **Test on another machine** (recommended)
   - Copy .exe to different PC
   - Verify it runs without Python
   - Check all features work

4. **Prepare documentation**
   - Include `README.txt`
   - Include `QUICK_REFERENCE.txt`
   - Optional: Full documentation from `product presentation\`

5. **Package for distribution**
   - Option 1: Just `SoundManager.exe`
   - Option 2: Zip with documentation
   - Option 3: Installer (advanced)

---

## 🎓 Advanced Topics

### Custom Icon

Replace `sound_manager_icon.ico` with your own:

1. Create or download .ico file (256x256 recommended)
2. Name it `sound_manager_icon.ico`
3. Place in project directory
4. Rebuild

---

### Version Information

Add version info to executable:

1. Create `version.txt`:
   ```
   VSVersionInfo(
     ffi=FixedFileInfo(
       filevers=(1, 0, 0, 0),
       prodvers=(1, 0, 0, 0),
       ...
     ),
     ...
   )
   ```

2. Add to build command:
   ```bash
   --version-file=version.txt
   ```

---

### Code Signing (Remove SmartScreen Warning)

1. **Get code signing certificate**
   - Purchase from CA (DigiCert, Sectigo, etc.)
   - Or use self-signed (still shows warning)

2. **Sign the executable**
   ```bash
   signtool sign /f certificate.pfx /p password /t http://timestamp.digicert.com dist\SoundManager.exe
   ```

3. **Distribute signed .exe**
   - No SmartScreen warning
   - Shows your company name

---

## 📝 Build Checklist

### Pre-Build

- [ ] Python installed and in PATH
- [ ] Source files exist (`sound_manager_gui.py`, icon)
- [ ] PyInstaller installed (or will auto-install)
- [ ] In correct directory

### Build

- [ ] Run `build_exe.bat` or `python build_exe.py`
- [ ] Wait for completion (1-2 minutes)
- [ ] Check for errors

### Post-Build

- [ ] Verify `dist\SoundManager.exe` exists
- [ ] Check file size (~49 MB)
- [ ] Test executable launches
- [ ] Test all features work
- [ ] Icon appears correctly

### Distribution

- [ ] Test on another machine (recommended)
- [ ] Prepare documentation
- [ ] Choose distribution method
- [ ] Share with colleagues

---

## 🎉 Success!

You now know how to:

✅ Build the executable from source  
✅ Rebuild after making changes  
✅ Troubleshoot common issues  
✅ Optimize the build process  
✅ Prepare for distribution  

**Happy building!** 🔨

---

## 📞 Quick Reference

| Task | Command |
|------|---------|
| **First build** | `build_exe.bat` |
| **Quick rebuild** | `REBUILD.bat` |
| **Python build** | `python build_exe.py` |
| **Using spec** | `pyinstaller SoundManager.spec` |
| **Install PyInstaller** | `pip install pyinstaller` |
| **Test executable** | `dist\SoundManager.exe` |

---

*For distribution instructions, see `DISTRIBUTION_GUIDE.md`*
