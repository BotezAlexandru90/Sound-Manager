# 📖 User Guide

<div align="center">

## 🎓 Master Sound Manager in 5 Minutes

**Step-by-step instructions for every feature**

</div>

---

## 🚀 Getting Started

### First Launch

1. **Double-click** `sound_manager_gui.py` or the executable
2. The window appears in the **bottom-right corner**
3. Apps playing audio appear **automatically**

```
┌─────────────────────────────────────────┐
│ SOUND MANAGER                      — ✕  │
├─────────────────────────────────────────┤
│ No active audio sessions                │ ← If nothing is playing
├─────────────────────────────────────────┤
│ 0 apps monitored              ⚙  ?     │
└─────────────────────────────────────────┘
```

**💡 Tip:** Play some music or video to see apps appear!

---

## 🎚️ Basic Controls

### 🔊 Adjust Volume

**Method 1: Drag the Slider**
```
1. Click and hold the blue slider handle
2. Drag left (quieter) or right (louder)
3. Release when done
```

**Method 2: Click the Bar**
```
1. Click anywhere on the slider bar
2. Volume jumps to that position instantly
```

**Visual Feedback:**
```
Before:  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 50%
         ↓ Drag right
After:   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 75%  ✨
```

---

### 🔇 Mute/Unmute

**One-Click Mute:**
```
Click 🔊 → Becomes 🔇 (Red) → Audio muted
Click 🔇 → Becomes 🔊 (Green) → Audio restored
```

**States:**
| Icon | Color | Status | Click to... |
|------|-------|--------|-------------|
| 🔊 | 🟢 Green | Playing | Mute |
| 🔇 | 🔴 Red | Muted | Unmute |

**💡 Pro Tip:** Muting doesn't change the slider position!

---

## 🙈 Exclusions System

### Quick Exclude (Right-Click)

**When to use:** You want to quickly hide an app

**Steps:**
```
1. Right-click on any app in the list
   ┌─────────────────────────────┐
   │ Exclude from monitoring     │
   └─────────────────────────────┘

2. Click "Exclude from monitoring"

3. App disappears immediately ✨
```

**Example:**
```
Before:                          After:
┌──────────────────────┐        ┌──────────────────────┐
│ Spotify      🔊      │        │ Chrome       🔊      │
│ Chrome       🔊      │        │ Discord      🔊      │
│ Discord      🔊      │        └──────────────────────┘
└──────────────────────┘        
   ↑ Right-click Spotify
```

---

### Manage Exclusions (Settings ⚙️)

**When to use:** You want to see all exclusions or add apps manually

#### **Opening the Settings**

```
1. Click the ⚙️ button in the footer
   
2. Exclusions dialog appears:

┌───────────────────────────────────────┐
│ Excluded Applications            ✕    │
├───────────────────────────────────────┤
│ Applications in this list will not be │
│ monitored for volume control.         │
├───────────────────────────────────────┤
│ ┌───────────────────────────────────┐ │
│ │ chrome.exe                        │ │ ← Your exclusions
│ │ spotify.exe                       │ │
│ └───────────────────────────────────┘ │
├───────────────────────────────────────┤
│ [Add Executable...] [Remove Selected] │
│                                       │
│            [Close]                    │
└───────────────────────────────────────┘
```

---

#### **Add an Executable Manually**

```
1. Click "Add Executable..." button

2. File picker opens:
   ┌─────────────────────────────────┐
   │ Select Executable to Exclude    │
   ├─────────────────────────────────┤
   │ 📁 Program Files                │
   │   📁 Google                     │
   │     📁 Chrome                   │
   │       ⚙️ chrome.exe  ← Select  │
   └─────────────────────────────────┘

3. Click "Open"

4. App added to exclusions list ✓
```

**💡 Use Case:** Exclude apps that aren't currently running

---

#### **Remove from Exclusions (Re-enable)**

```
1. Open settings (⚙️ button)

2. Click on the app you want to re-enable:
   ┌───────────────────────────────────┐
   │ chrome.exe      ← Click to select │
   │ spotify.exe                       │
   └───────────────────────────────────┘

3. Click "Remove Selected" button

4. App removed from exclusions ✓

5. Click "Close"

6. App will reappear when it plays audio! 🎉
```

---

## 🪟 Window Management

### Move the Window

```
1. Click anywhere on the window (except buttons/sliders)
2. Hold and drag
3. Release at desired position
4. Position saved automatically 💾
```

**💡 Tip:** Drag from the header or empty spaces!

---

### Resize the Window

```
1. Move mouse to left or right edge
2. Cursor changes to ↔️
3. Click and drag to resize
4. Width: 200px (min) to 1000px (max)
5. Size saved automatically 💾
```

**Visual Guide:**
```
┌─────────────────────────────────────────┐
↔️                                        ↔️
Left edge                         Right edge
(Drag to resize)                 (Drag to resize)
```

---

### Minimize

```
Click the "—" button → Window minimizes to taskbar
Click taskbar icon → Window restores
```

---

### Close

```
Click the "✕" button → App closes
All settings saved automatically ✓
```

---

## 📊 Understanding the Status Bar

```
┌─────────────────────────────────────────┐
│ 5 apps monitored (2 excluded)    ⚙  ?  │
└─────────────────────────────────────────┘
  ↑                  ↑               ↑  ↑
  Active count    Hidden count      Settings Help
```

**What it tells you:**
- **"5 apps monitored"** → 5 apps currently visible
- **(2 excluded)** → 2 apps hidden via exclusions
- **⚙️** → Open exclusions settings
- **?** → Open about dialog

---

## 🎯 Common Workflows

### Scenario 1: Gaming + Music

**Goal:** Lower music volume while gaming

```
1. Launch game and music player
2. Both appear in Sound Manager
3. Drag music slider to 30%
4. Drag game slider to 80%
5. Perfect balance! 🎮🎵
```

---

### Scenario 2: Video Call + Browser

**Goal:** Mute browser during important call

```
1. Join video call (Discord/Zoom)
2. Browser playing video
3. Click 🔊 on browser → Becomes 🔇
4. Focus on call without distractions
5. Click 🔇 when call ends → Sound restored
```

---

### Scenario 3: Clean Up Clutter

**Goal:** Hide apps you never adjust

```
1. Right-click "System Sounds" → Exclude
2. Right-click "Windows Notifications" → Exclude
3. Right-click "Background App" → Exclude
4. Now only see apps you care about! ✨
```

---

### Scenario 4: Re-enable Hidden App

**Goal:** Bring back an excluded app

```
1. Click ⚙️ (settings)
2. Find app in exclusions list
3. Click to select it
4. Click "Remove Selected"
5. Click "Close"
6. App appears when it plays audio! 🎉
```

---

## 💡 Pro Tips & Tricks

### Tip 1: Quick Mute All
```
Click 🔊 on each app → All muted
Perfect for sudden interruptions! 🤫
```

### Tip 2: Fine Control
```
Click near current position for small adjustments
Drag for big changes
```

### Tip 3: Monitor Count
```
Keep an eye on the status bar
"(X excluded)" reminds you of hidden apps
```

### Tip 4: Window Position
```
Place Sound Manager in a corner
It stays on top but doesn't block content
```

### Tip 5: Hover for Info
```
Hover over excluded apps → See full path
Hover over buttons → See tooltips
```

---

## 🎨 Customization

### What You Can Customize:

✅ **Window Position** → Drag anywhere  
✅ **Window Width** → Resize edges (200-1000px)  
✅ **Visible Apps** → Exclude/include as needed  

### What's Automatic:

🤖 **Window Height** → Adjusts to app count  
🤖 **App Discovery** → Detects audio automatically  
🤖 **Volume Sync** → Updates every 200ms  
🤖 **Settings Save** → No manual save needed  

---

## 🆘 Troubleshooting

### App Doesn't Appear

**Check:**
1. ✅ Is the app playing audio?
2. ✅ Is it in exclusions? (Click ⚙️ to check)
3. ✅ Wait 5 seconds (refresh interval)

**Solution:** Play audio in the app or remove from exclusions

---

### Volume Slider Not Moving

**Check:**
1. ✅ Are you dragging the slider?
2. ✅ Sync pauses during drag

**Solution:** Release the slider, it will sync in 200ms

---

### Window Off-Screen

**Check:**
1. ✅ Multiple monitors disconnected?
2. ✅ Resolution changed?

**Solution:** Delete `config.json`, restart app (resets position)

---

### Exclusion Not Working

**Check:**
1. ✅ Correct .exe file selected?
2. ✅ Full path matches?

**Solution:** Hover over exclusion to see path, verify it's correct

---

## 🎓 Quick Reference

| Action | How To |
|--------|--------|
| **Adjust Volume** | Drag slider or click bar |
| **Mute** | Click 🔊 button |
| **Unmute** | Click 🔇 button |
| **Exclude App** | Right-click → Exclude |
| **Re-enable App** | ⚙️ → Select → Remove |
| **Add Manually** | ⚙️ → Add Executable |
| **Move Window** | Drag anywhere |
| **Resize Window** | Drag left/right edge |
| **Minimize** | Click — |
| **Close** | Click ✕ |
| **About** | Click ? |

---

<div align="center">

### 🎉 You're Now a Sound Manager Expert!

**Next:** [Technical Details](04_TECHNICAL.md) → Learn how it works! 🔧

</div>
