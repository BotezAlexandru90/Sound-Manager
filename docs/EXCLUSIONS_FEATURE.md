# Exclusions Feature Documentation

## Overview
The exclusions feature allows users to hide specific applications from the monitoring list. Excluded applications will not appear in the Sound Manager interface and will not be monitored for volume control.

## User Interface

### 1. Settings Button (Cogwheel Icon)
- **Location**: Bottom footer, next to the "?" help button
- **Icon**: ⚙ (cogwheel)
- **Tooltip**: "Exclusions"
- **Function**: Opens the Exclusions Dialog

### 2. Context Menu (Right-Click)
- **Where**: Right-click on any application in the monitoring list
- **Menu Option**: "Exclude from monitoring"
- **Function**: Immediately excludes the application and removes it from the list

### 3. Exclusions Dialog
A dedicated window for managing excluded applications.

#### Features:
- **Title**: "Excluded Applications"
- **Description**: "Applications in this list will not be monitored for volume control."
- **List View**: Shows all currently excluded applications
  - Displays executable name (e.g., "chrome.exe")
  - Tooltip shows full path on hover
  - Sorted alphabetically
  
#### Buttons:
1. **Add Executable...**: Opens file picker to manually add an .exe file to exclusions
2. **Remove Selected**: Removes the selected application from exclusions (re-enables monitoring)
3. **Close**: Closes the dialog

## How It Works

### Excluding an Application
**Method 1: Right-Click (Quick)**
1. Right-click on any application in the monitoring list
2. Click "Exclude from monitoring"
3. The application immediately disappears from the list

**Method 2: Manual Addition**
1. Click the cogwheel (⚙) button in the footer
2. Click "Add Executable..." button
3. Browse and select the .exe file
4. Click Open
5. The application is added to the exclusions list

### Re-enabling a Monitored Application
1. Click the cogwheel (⚙) button in the footer
2. Find the application in the exclusions list
3. Select it
4. Click "Remove Selected"
5. The application will reappear in the monitoring list (if it's currently running audio)

## Technical Details

### Data Storage
- **File**: `exclusions.json` (stored in the same directory as the application)
- **Format**: JSON array of executable file paths
- **Example**:
```json
[
  "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
  "C:\\Program Files\\Spotify\\Spotify.exe"
]
```

### Persistence
- Exclusions are saved immediately when modified
- Exclusions persist across application restarts
- Exclusions are loaded on application startup

### Filtering Logic
- During session refresh, each audio session is checked against the exclusions list
- If the session's executable path matches any exclusion, it's skipped
- System sounds (sessions without a process) are never excluded

### Status Display
- The footer status label shows monitored app count
- When exclusions exist, it also shows the count: "3 apps monitored (2 excluded)"

## UI Styling

### Exclusions Dialog
- **Size**: 400x350 pixels
- **Style**: Matches the main application's dark theme
- **Colors**:
  - Background: #252525
  - List background: #1e1e1e
  - Borders: #3c3c3c
  - Accent: #0078d7 (blue)
  - Text: #E0E0E0

### Context Menu
- **Style**: Dark theme matching the application
- **Background**: #2d2d2d
- **Hover**: #0078d7 (blue)
- **Border**: #3c3c3c

## Implementation Details

### New Components

1. **ExclusionsDialog Class**
   - Custom QDialog with frameless window
   - Draggable interface
   - Signal: `exclusions_changed` (emitted when list is modified)
   - Methods:
     - `add_executable()`: File picker for manual addition
     - `remove_selected()`: Removes selected item
     - `get_exclusions()`: Returns current exclusions list

2. **AudioSessionWidget Enhancement**
   - Signal: `exclude_requested(str)` (emits executable path)
   - Context menu support
   - Stores executable path for exclusion

3. **SoundManagerApp Enhancement**
   - Loads/saves exclusions from/to JSON file
   - Filters sessions based on exclusions
   - Connects exclusion signals
   - Updates status label with exclusion count

### Files Modified
- `sound_manager_gui.py`: Main application file
  - Added ExclusionsDialog class
  - Enhanced AudioSessionWidget with context menu
  - Added exclusion management to SoundManagerApp
  - Added cogwheel button to footer

### New Files Created
- `exclusions.json`: Stores excluded application paths (auto-created)

## Benefits

1. **Cleaner Interface**: Hide applications you don't need to control
2. **Focus**: Only see the applications you actively manage
3. **Performance**: Slightly reduced overhead by not monitoring excluded apps
4. **Flexibility**: Easy to add/remove exclusions at any time
5. **Persistent**: Exclusions remembered across sessions

## Use Cases

- Exclude system applications you never adjust (e.g., Windows sounds)
- Hide background applications (e.g., update services)
- Reduce clutter when many applications are playing audio
- Focus on specific applications (e.g., only show media players)

## Future Enhancements (Not Implemented)

Potential future improvements:
- Import/export exclusions list
- Exclude by process name pattern (e.g., all "chrome.exe" instances)
- Temporary exclusions (session-only)
- Quick toggle to show/hide excluded apps
- Exclusion presets (e.g., "Gaming", "Work", "Media")
