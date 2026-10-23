# 💡 FAQ & Tips

<div align="center">

## ❓ Frequently Asked Questions

**Quick answers to common questions**

</div>

---

## 🎯 General Questions

### Q: What is Sound Manager?

**A:** Sound Manager is a lightweight Windows application that gives you **per-application volume control** in a clean, always-accessible interface. Think of it as a better, faster alternative to Windows Volume Mixer!

---

### Q: Is it free?

**A:** Yes! 100% free and open-source. No ads, no subscriptions, no hidden costs. 🎉

---

### Q: Does it work on Mac/Linux?

**A:** No, it's **Windows-only** (Windows 10/11). It uses Windows-specific audio APIs that aren't available on other platforms.

---

### Q: Do I need admin rights?

**A:** **No!** Sound Manager runs as a standard user. No elevation required. 🔓

---

### Q: Does it collect my data?

**A:** **Absolutely not!** 
- ❌ No telemetry
- ❌ No analytics
- ❌ No network access
- ✅ 100% offline
- ✅ All data stays local

---

## 🔧 Technical Questions

### Q: Why does it need Python?

**A:** Sound Manager is written in Python for:
- ✅ Rapid development
- ✅ Easy maintenance
- ✅ Cross-version compatibility
- ✅ Rich library ecosystem

**Note:** Standalone .exe versions don't need Python installed!

---

### Q: How much RAM does it use?

**A:** Very little!
- **Idle:** ~18 MB
- **Active:** ~20 MB
- **With 10 apps:** ~22 MB

For comparison, Chrome uses **200-500 MB** per tab! 😄

---

### Q: Does it slow down my PC?

**A:** **No!** CPU usage is typically **<1%**. It's extremely lightweight and won't impact performance.

---

### Q: Can I run it at startup?

**A:** Yes! Add it to your Windows Startup folder:

```
1. Press Win + R
2. Type: shell:startup
3. Press Enter
4. Copy Sound Manager shortcut here
```

---

### Q: How does it detect applications?

**A:** It uses the **Windows Core Audio API** to discover audio sessions. When an app plays sound, Windows registers it, and Sound Manager detects it automatically!

---

## 🎵 Usage Questions

### Q: Why doesn't my app appear?

**Possible reasons:**

1. **Not playing audio** → Play something!
2. **In exclusions list** → Check settings (⚙️)
3. **Just launched** → Wait 5 seconds (refresh interval)
4. **System audio session** → Some apps use shared sessions

**Solution:** Make sure it's playing audio and not excluded.

---

### Q: Can I control system sounds?

**A:** Yes! If "System Sounds" appears in the list, you can control it. Some systems don't expose it as a separate session.

---

### Q: Why does the slider jump back?

**A:** You might be adjusting volume in **two places at once**:
- Sound Manager
- Windows Volume Mixer
- App's own controls

Sound Manager syncs every 200ms, so it updates to match the actual volume.

---

### Q: Can I set volume above 100%?

**A:** **No.** Windows limits volume to 100%. Some apps have internal boost, but that's controlled by the app itself, not Windows.

---

### Q: Does muting here mute in Windows?

**A:** **Yes!** Sound Manager controls the **same volume** as Windows Volume Mixer. Changes sync both ways.

---

## 🙈 Exclusions Questions

### Q: What happens to excluded apps?

**A:** They're **hidden from the list** but still play audio normally. Sound Manager just doesn't show or control them.

---

### Q: Are exclusions permanent?

**A:** **Yes!** They're saved to `exclusions.json` and persist across:
- ✅ Application restarts
- ✅ System reboots
- ✅ Updates

---

### Q: Can I exclude system sounds?

**A:** Yes! Right-click "System Sounds" and exclude it, or add it manually via settings.

---

### Q: How do I see what's excluded?

**A:** Click the **⚙️ (cogwheel)** button in the footer. All exclusions are listed there.

---

### Q: Can I export my exclusions?

**A:** Currently no, but you can manually copy `exclusions.json` to backup or share your exclusions list.

---

## 🪟 Window Questions

### Q: Can I resize the window?

**A:** **Width:** Yes! Drag left or right edge (200-1000px)  
**Height:** No, it auto-adjusts based on app count

---

### Q: Why is it always on top?

**A:** By design! This keeps it accessible without hunting through windows. You can minimize it if needed.

---

### Q: Can I disable "always on top"?

**A:** Not currently. It's a core feature to keep controls accessible. You can minimize when not needed.

---

### Q: The window is off-screen, how do I reset it?

**A:** 
```
1. Close Sound Manager
2. Delete config.json
3. Restart Sound Manager
4. Window appears in default position
```

---

### Q: Does it remember my position?

**A:** **Yes!** Position and size are saved automatically every time you move or resize.

---

## 🐛 Troubleshooting

### Q: App crashed, what do I do?

**A:** 
1. Restart Sound Manager
2. Check if issue persists
3. Try deleting `config.json` and `exclusions.json`
4. Reinstall if needed

**Note:** Crashes are rare! The app has robust error handling.

---

### Q: Volume slider doesn't move

**Possible causes:**

1. **You're dragging it** → Sync pauses during drag
2. **App is muted** → Unmute first
3. **App crashed** → Restart the app

**Solution:** Release slider and wait 200ms for sync.

---

### Q: Icons don't show

**A:** Icons are loaded from the executable. If missing:
- App might not have an icon
- Executable path is inaccessible
- Permission issue

**Impact:** Purely visual, doesn't affect functionality.

---

### Q: Settings not saving

**A:** Check:
1. ✅ Write permissions in app directory
2. ✅ Disk space available
3. ✅ Antivirus not blocking

**Solution:** Run from a folder you have write access to.

---

## 💡 Pro Tips

### Tip #1: Quick Mute for Meetings 🎤

```
Keep Sound Manager visible
When meeting starts → Click 🔊 on each app
Instant silence! 🤫
```

---

### Tip #2: Gaming Setup 🎮

```
Exclude background apps:
- Game launchers
- Update services
- System sounds

Keep only:
- Game
- Voice chat
- Music player

Clean, focused control! ✨
```

---

### Tip #3: Productivity Mode 💼

```
Lower all apps to 20-30%
Except:
- Video conferencing (100%)
- Notification sounds (50%)

Stay focused, hear what matters! 🎯
```

---

### Tip #4: Movie Night 🎬

```
Mute everything except media player
No interruptions from:
- Email notifications
- Chat apps
- Browser tabs

Pure entertainment! 🍿
```

---

### Tip #5: Fine-Tuning 🎚️

```
For precise control:
1. Click near current position
2. Small adjustments: Click slider bar
3. Big changes: Drag slider
4. Mute/unmute: Use button, not 0%
```

---

## 🎨 Customization Tips

### Tip #6: Window Placement 📍

**Best positions:**
- **Bottom-right:** Default, unobtrusive
- **Top-right:** Quick access
- **Second monitor:** Dedicated control panel

---

### Tip #7: Width Sizing 📏

**Recommendations:**
- **200px:** Minimal, icon + slider
- **300px:** Balanced (default)
- **500px+:** Full app names visible

---

### Tip #8: Exclusion Strategy 🙈

**What to exclude:**
- ✅ Apps you never adjust
- ✅ System sounds
- ✅ Background services
- ✅ Update notifications

**What to keep:**
- ✅ Media players
- ✅ Games
- ✅ Communication apps
- ✅ Browsers

---

## 🚀 Advanced Tips

### Tip #9: Multi-Monitor Setup 🖥️🖥️

```
Place Sound Manager on secondary monitor
Full-screen game on primary
Control audio without Alt+Tab! 🎮
```

---

### Tip #10: Keyboard + Mouse Combo ⌨️🖱️

```
1. Position Sound Manager in corner
2. Memorize app positions
3. Quick muscle-memory adjustments
4. No need to look! 🚀
```

---

### Tip #11: Backup Your Settings 💾

```
Copy these files to backup:
- config.json (window settings)
- exclusions.json (hidden apps)

Restore anytime! ✓
```

---

## 📊 Performance Tips

### Tip #12: Minimize When Not Needed 📉

```
Click "—" to minimize
Reduces visual clutter
Still runs in background
Restore from taskbar
```

---

### Tip #13: Clean Exclusions List 🧹

```
Periodically review exclusions:
1. Click ⚙️
2. Remove apps you uninstalled
3. Keep list current

Faster, cleaner! ✨
```

---

## 🎯 Workflow Tips

### Tip #14: Create Presets (Manual) 📋

```
Take screenshots of slider positions for:
- Gaming preset
- Work preset
- Movie preset
- Music preset

Recreate quickly when needed! 📸
```

---

### Tip #15: Pair with Hotkeys 🔥

```
Use Windows hotkeys:
- Win + B: Focus system tray
- Win + D: Show desktop (reveal Sound Manager)
- Alt + Tab: Quick switch

Combine with Sound Manager for power! ⚡
```

---

## 🔮 Future Features (Wishlist)

**What users are asking for:**

1. 🎨 Theme customization
2. ⌨️ Keyboard shortcuts
3. 📊 Volume presets
4. 🔔 System tray integration
5. 📈 Volume history
6. 🎯 Per-app equalizer
7. 🌐 Multi-language support
8. 🔊 Volume boost (>100%)

**Note:** These are not implemented yet, but could be in future versions!

---

## 📞 Support & Feedback

### Q: How do I report a bug?

**A:** Check the application's repository or documentation for issue reporting guidelines.

---

### Q: Can I request a feature?

**A:** Yes! Feature requests are welcome. Check the project's GitHub or contact channels.

---

### Q: How can I contribute?

**A:** The project is open-source! You can:
- 🐛 Report bugs
- 💡 Suggest features
- 📝 Improve documentation
- 💻 Submit code

---

## 🎓 Learning Resources

### Want to Learn More?

1. **[Welcome Guide](01_WELCOME.md)** → Overview
2. **[Features](02_FEATURES.md)** → Capabilities
3. **[User Guide](03_USER_GUIDE.md)** → How-to
4. **[Technical](04_TECHNICAL.md)** → Architecture
5. **[FAQ](05_FAQ.md)** → You are here! ✓

---

## 🎉 Quick Wins

### New User Checklist:

- [ ] Launch Sound Manager
- [ ] Play audio in 2-3 apps
- [ ] Adjust a volume slider
- [ ] Mute an app
- [ ] Right-click to exclude an app
- [ ] Open settings (⚙️)
- [ ] Re-enable an excluded app
- [ ] Move the window
- [ ] Resize the window
- [ ] Check the status bar

**Completed all?** You're a Sound Manager pro! 🏆

---

<div align="center">

## 🎊 That's All!

You now know everything about Sound Manager!

### 🚀 Go forth and control your audio like a boss! 🎵

---

**Questions not answered here?**  
Check the other guides or reach out for support!

**Happy listening!** 🎧

</div>
