# Sound Manager - Quick Usage Guide

## Main Interface

```
┌─────────────────────────────────────────┐
│ SOUND MANAGER                      — ✕  │  ← Header with minimize/close
├─────────────────────────────────────────┤
│  🎵 Spotify                         🔊  │  ← Application with icon & mute
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  75% │  ← Volume slider
│                                         │
│  🌐 Chrome                          🔊  │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  50% │
│                                         │
│  🎮 Game.exe                        🔊  │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100% │
├─────────────────────────────────────────┤
│ 3 apps monitored              ⚙  ?     │  ← Footer with settings & help
└─────────────────────────────────────────┘
                                  ↑  ↑
                            Settings About
```

## Features

### Volume Control
- **Slider**: Drag to adjust volume (0-100%)
- **Percentage**: Shows current volume level
- **Mute Button**: 🔊 (unmuted) / 🔇 (muted)
  - Green when unmuted
  - Red when muted

### Window Controls
- **Drag**: Click and drag anywhere to move window
- **Resize**: Drag left or right edge to resize width
- **Height**: Automatically adjusts based on number of apps
- **Minimize**: Click "—" button
- **Close**: Click "✕" button

### Exclusions (NEW!)

#### Quick Exclude (Right-Click)
```
Right-click on any app
    ↓
┌─────────────────────────────┐
│ Exclude from monitoring     │
└─────────────────────────────┘
    ↓
App disappears from list
```

#### Manage Exclusions (Settings)
```
Click ⚙ button
    ↓
┌───────────────────────────────────────┐
│ Excluded Applications            ✕    │
├───────────────────────────────────────┤
│ Applications in this list will not be │
│ monitored for volume control.         │
├───────────────────────────────────────┤
│ ┌───────────────────────────────────┐ │
│ │ chrome.exe                        │ │
│ │ spotify.exe                       │ │
│ │ discord.exe                       │ │
│ └───────────────────────────────────┘ │
├───────────────────────────────────────┤
│ [Add Executable...] [Remove Selected] │
│                                       │
│            [Close]                    │
└───────────────────────────────────────┘
```

## Common Tasks

### Exclude an Application
**Option 1 (Quick):**
1. Right-click the application
2. Click "Exclude from monitoring"
✓ Done!

**Option 2 (Manual):**
1. Click ⚙ (settings)
2. Click "Add Executable..."
3. Browse to the .exe file
4. Click Open
✓ Done!

### Re-enable an Excluded Application
1. Click ⚙ (settings)
2. Select the application from the list
3. Click "Remove Selected"
4. Click "Close"
✓ The app will appear when it plays audio

### Adjust Volume
- **Method 1**: Drag the slider
- **Method 2**: Click anywhere on the slider bar
- **Tip**: Changes apply instantly

### Mute/Unmute
- Click the 🔊/🔇 button
- **Green** = Sound on
- **Red** = Muted

## Tips & Tricks

1. **Persistent Settings**: Window position, size, and exclusions are saved automatically

2. **Real-time Sync**: Volume changes from other sources (Windows mixer, app controls) are reflected instantly

3. **Dynamic List**: Applications appear when they start playing audio and disappear when they stop

4. **Always on Top**: Window stays visible above other windows

5. **Status Info**: Footer shows:
   - Number of monitored apps
   - Number of excluded apps (if any)
   - Example: "3 apps monitored (2 excluded)"

6. **Tooltips**: Hover over buttons and excluded apps to see more info

7. **System Sounds**: The "System Sounds" entry (if present) cannot be excluded via right-click

## Keyboard Shortcuts

Currently, the application is mouse-driven. Keyboard shortcuts may be added in future versions.

## Troubleshooting

### Application doesn't appear in the list
- Make sure it's playing audio
- Check if it's in the exclusions list (⚙ settings)
- Some apps may not register as separate audio sessions

### Exclusion not working
- Ensure you excluded the correct .exe file
- Check the full path in the exclusions list (hover for tooltip)
- Restart the excluded application

### Window position resets
- The position is saved on move/resize
- If the saved position is off-screen, it will reset to default

### Volume slider doesn't match actual volume
- The slider syncs every 200ms
- If you're dragging the slider, sync is paused
- Release the slider to allow sync

## File Locations

All configuration files are stored in the application directory:

- `config.json`: Window position and size
- `exclusions.json`: List of excluded applications
- `sound_manager_icon.ico`: Application icon

## Support

For issues or feedback, refer to the application's repository or documentation.
