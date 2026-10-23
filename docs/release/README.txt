================================================================================
                          SOUND MANAGER v1.0
================================================================================

WHAT IT DOES
------------
Sound Manager gives you independent volume control for each application.
Control music, games, browsers, and calls separately - all in one window!

QUICK START
-----------
1. Double-click SoundManager.exe
2. Play audio in any app (Spotify, Chrome, etc.)
3. Apps appear automatically in Sound Manager
4. Drag sliders to adjust volume
5. Click speaker icons (🔊/🔇) to mute/unmute

KEY FEATURES
------------
✓ Per-application volume sliders (0-100%)
✓ Individual mute/unmute buttons
✓ Right-click any app to hide it from the list
✓ Settings button (⚙) to manage hidden apps
✓ Always-on-top window for quick access
✓ Auto-saves position and settings

SYSTEM REQUIREMENTS
-------------------
• Windows 10 or Windows 11 (64-bit)
• 100 MB RAM
• 50 MB disk space
• That's it! No Python or other software needed.

HOW TO USE
----------

ADJUST VOLUME:
  • Drag the slider left (quieter) or right (louder)
  • Or click anywhere on the slider bar

MUTE/UNMUTE:
  • Click the speaker icon 🔊 to mute
  • Click 🔇 to unmute
  • Green = unmuted, Red = muted

HIDE APPS:
  • Right-click any app → "Exclude from monitoring"
  • App disappears from the list

SHOW HIDDEN APPS:
  • Click the ⚙ (cogwheel) button
  • Select app → Click "Remove Selected"
  • App reappears when it plays audio

MOVE WINDOW:
  • Click and drag anywhere to move
  • Drag left or right edge to resize width
  • Position is saved automatically

COMMON SCENARIOS
----------------

Gaming + Music:
  1. Launch game and music player
  2. Lower music to 30%
  3. Keep game at 80%
  4. Perfect balance!

Video Call:
  1. Join call (Zoom, Teams, etc.)
  2. Mute browser/music with one click
  3. Focus on the call
  4. Unmute when done

Clean Interface:
  1. Right-click apps you never adjust
  2. Exclude them from monitoring
  3. See only what matters!

TROUBLESHOOTING
---------------

Q: My app doesn't appear in the list
A: • Make sure the app is playing audio
   • Wait 5 seconds (refresh interval)
   • Check if it's in the exclusions list (⚙ button)

Q: Windows shows a security warning
A: • This is normal for unsigned executables
   • Click "More info" → "Run anyway"
   • The file is safe - just not digitally signed

Q: Antivirus blocks the file
A: • Add SoundManager.exe to your antivirus whitelist
   • Or scan it with VirusTotal to verify it's safe
   • This is a common false positive with PyInstaller apps

Q: Volume slider doesn't move
A: • Release the slider (sync pauses during drag)
   • Wait 200ms for automatic sync

Q: Settings don't save
A: • Make sure you have write permissions in the folder
   • Settings are saved to config.json automatically

Q: Window is off-screen
A: • Delete config.json in the same folder as the .exe
   • Restart Sound Manager
   • Window appears in default position

TIPS & TRICKS
-------------

💡 Place the window in a corner - it stays on top but doesn't block content

💡 Use exclusions to hide background apps you never adjust

💡 The status bar shows how many apps are monitored and excluded

💡 Hover over excluded apps in settings to see their full path

💡 Minimize the window when not needed - it keeps running

TECHNICAL INFO
--------------

File: SoundManager.exe
Size: ~49 MB (includes all dependencies)
Type: Standalone executable
Platform: Windows 10/11 (64-bit)
Memory: ~20 MB when running
CPU: <1% (very lightweight)

WHAT'S INCLUDED
---------------
This single .exe file contains everything needed:
• Python interpreter
• PyQt6 GUI framework
• Windows audio control libraries
• All dependencies
• Application icon

No installation required!
No additional files needed!
Just run and enjoy!

FILES CREATED
-------------
When you run Sound Manager, it creates:
• config.json - Window position and size
• exclusions.json - List of hidden apps

Both files are in the same folder as SoundManager.exe

PRIVACY & SECURITY
------------------
✓ No internet connection required
✓ No data collection or telemetry
✓ No analytics or tracking
✓ All data stays on your computer
✓ No admin rights needed

SUPPORT
-------
For questions or issues, contact your IT administrator or the person
who shared this tool with you.

For documentation, see the "product presentation" folder (if included).

CREDITS
-------
Created by Digital Epoch
Version 1.0
2026

================================================================================
                        Enjoy Sound Manager!
================================================================================
