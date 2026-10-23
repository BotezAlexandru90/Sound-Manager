import sys
import os
import json
import signal
from typing import Optional, List, Dict, Tuple
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QPushButton, 
                             QHBoxLayout, QLabel, QFrame, QSlider, QScrollArea,
                             QFileIconProvider, QSizePolicy, QDialog, QMenu, 
                             QListWidget, QListWidgetItem, QFileDialog, QMessageBox)
from PyQt6.QtCore import Qt, QTimer, QFileInfo, QEvent, pyqtSignal
from PyQt6.QtGui import QMouseEvent, QIcon, QPixmap, QAction, QCursor
from pycaw.pycaw import AudioUtilities, ISimpleAudioVolume
import win32gui  # type: ignore[reportMissingImports]
import win32process  # type: ignore[reportMissingImports]

SYNC_TIMER_MS = 200
REFRESH_TIMER_MS = 5000
ITEM_HEIGHT_PX = 58
HEADER_HEIGHT_PX = 35
FOOTER_HEIGHT_PX = 26
UI_MARGIN_PX = 12
MAX_WINDOW_HEIGHT_PX = 600
RESIZE_MARGIN_PX = 6
MIN_WINDOW_WIDTH_PX = 200
MAX_WINDOW_WIDTH_PX = 1000
DEFAULT_WINDOW_WIDTH_PX = 300

if getattr(sys, 'frozen', False):
    BASE_DIR = os.path.dirname(sys.executable)
    CONFIG_FILE = os.path.join(BASE_DIR, "config.json")
    EXCLUSIONS_FILE = os.path.join(BASE_DIR, "exclusions.json")
    APP_ICON_PATH = os.path.join(getattr(sys, '_MEIPASS', BASE_DIR), "sound_manager_icon.ico")
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    CONFIG_FILE = os.path.join(BASE_DIR, "config.json")
    EXCLUSIONS_FILE = os.path.join(BASE_DIR, "exclusions.json")
    APP_ICON_PATH = os.path.join(BASE_DIR, "sound_manager_icon.ico")

def get_window_title(pid: int) -> Optional[str]:
    """Gets the window title for a given PID."""
    def callback(hwnd, titles):
        if win32gui.IsWindowVisible(hwnd):
            _, found_pid = win32process.GetWindowThreadProcessId(hwnd)
            if found_pid == pid:
                text = win32gui.GetWindowText(hwnd)
                if text:
                    titles.append(text)
        return True
    
    titles = []
    try:
        win32gui.EnumWindows(callback, titles)
    except Exception:
        pass
    return titles[0] if titles else None

def get_session_id(session) -> str:
    """Generates a unique identifier for an audio session."""
    try:
        if hasattr(session, "InstanceIdentifier") and session.InstanceIdentifier:
            return str(session.InstanceIdentifier)
        if hasattr(session, "Identifier") and session.Identifier:
            return str(session.Identifier)
    except Exception:
        pass
    
    pid = session.Process.pid if session.Process else "system"
    display_name = getattr(session, "DisplayName", "") or ""
    return f"{pid}_{display_name}"

class ElidedLabel(QLabel):
    def __init__(self, text: str = "", parent: Optional[QWidget] = None):
        super().__init__(text, parent)
        self.full_text: str = text
        self.setMinimumWidth(10)

    def setText(self, text: str) -> None:
        self.full_text = text
        self.setToolTip(text)
        self.update_elided_text()

    def text(self) -> str:
        return self.full_text if self.full_text is not None else ""

    def resizeEvent(self, event) -> None:
        self.update_elided_text()
        super().resizeEvent(event)

    def update_elided_text(self) -> None:
        if not self.full_text:
            super().setText("")
            return
        metrics = self.fontMetrics()
        elided = metrics.elidedText(self.full_text, Qt.TextElideMode.ElideRight, max(10, self.width()))
        super().setText(elided)

class ExclusionsDialog(QDialog):
    exclusions_changed = pyqtSignal()
    
    def __init__(self, exclusions: List[str], parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.exclusions = exclusions.copy()
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.Dialog)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setFixedSize(400, 350)
        self.drag_pos: Optional[object] = None
        self.setup_ui()

    def setup_ui(self) -> None:
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        frame = QFrame()
        frame.setStyleSheet("""
            QFrame {
                background-color: #252525;
                border: 1px solid #3c3c3c;
                border-radius: 10px;
            }
        """)
        frame_layout = QVBoxLayout(frame)
        frame_layout.setContentsMargins(14, 12, 14, 12)
        frame_layout.setSpacing(10)

        title_layout = QHBoxLayout()
        title_label = QLabel("Excluded Applications")
        title_label.setStyleSheet("color: #0078d7; font-weight: bold; font-size: 13px; border: none;")
        title_layout.addWidget(title_label)
        title_layout.addStretch()

        close_btn = QPushButton("✕")
        close_btn.setFixedSize(20, 20)
        close_btn.clicked.connect(self.accept)
        close_btn.setStyleSheet("""
            QPushButton { color: #888; border: none; font-size: 12px; background: transparent; }
            QPushButton:hover { color: white; background: #e81123; border-radius: 3px; }
        """)
        title_layout.addWidget(close_btn)
        frame_layout.addLayout(title_layout)

        desc_label = QLabel("Applications in this list will not be monitored for volume control.")
        desc_label.setWordWrap(True)
        desc_label.setStyleSheet("color: #999; font-size: 10px; border: none; background: transparent;")
        frame_layout.addWidget(desc_label)

        self.list_widget = QListWidget()
        self.list_widget.setStyleSheet("""
            QListWidget {
                background-color: #1e1e1e;
                color: #E0E0E0;
                border: 1px solid #3c3c3c;
                border-radius: 4px;
                padding: 4px;
                font-size: 10px;
            }
            QListWidget::item {
                padding: 6px;
                border-radius: 3px;
            }
            QListWidget::item:hover {
                background-color: #2a2a2a;
            }
            QListWidget::item:selected {
                background-color: #0078d7;
            }
        """)
        self.populate_list()
        frame_layout.addWidget(self.list_widget, 1)

        btn_layout = QHBoxLayout()
        
        add_btn = QPushButton("Add Executable...")
        add_btn.setFixedHeight(26)
        add_btn.clicked.connect(self.add_executable)
        add_btn.setStyleSheet("""
            QPushButton {
                background-color: #2d2d2d;
                color: #E0E0E0;
                font-size: 10px;
                border: 1px solid #3c3c3c;
                border-radius: 4px;
                padding: 4px 8px;
            }
            QPushButton:hover {
                background-color: #3c3c3c;
                border-color: #0078d7;
            }
        """)
        btn_layout.addWidget(add_btn)

        remove_btn = QPushButton("Remove Selected")
        remove_btn.setFixedHeight(26)
        remove_btn.clicked.connect(self.remove_selected)
        remove_btn.setStyleSheet("""
            QPushButton {
                background-color: #2d2d2d;
                color: #E0E0E0;
                font-size: 10px;
                border: 1px solid #3c3c3c;
                border-radius: 4px;
                padding: 4px 8px;
            }
            QPushButton:hover {
                background-color: #3c3c3c;
                border-color: #0078d7;
            }
        """)
        btn_layout.addWidget(remove_btn)
        frame_layout.addLayout(btn_layout)

        ok_btn = QPushButton("Close")
        ok_btn.setFixedHeight(28)
        ok_btn.clicked.connect(self.accept)
        ok_btn.setStyleSheet("""
            QPushButton {
                background-color: #0078d7;
                color: white;
                font-weight: 500;
                font-size: 11px;
                border: none;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #1084e3;
            }
        """)
        frame_layout.addWidget(ok_btn)

        main_layout.addWidget(frame)

    def populate_list(self) -> None:
        self.list_widget.clear()
        for exe_path in sorted(self.exclusions):
            exe_name = os.path.basename(exe_path)
            item = QListWidgetItem(f"{exe_name}")
            item.setToolTip(exe_path)
            item.setData(Qt.ItemDataRole.UserRole, exe_path)
            self.list_widget.addItem(item)

    def add_executable(self) -> None:
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Executable to Exclude",
            "",
            "Executable Files (*.exe);;All Files (*.*)"
        )
        if file_path and file_path not in self.exclusions:
            self.exclusions.append(file_path)
            self.populate_list()
            self.exclusions_changed.emit()

    def remove_selected(self) -> None:
        current_item = self.list_widget.currentItem()
        if current_item:
            exe_path = current_item.data(Qt.ItemDataRole.UserRole)
            if exe_path in self.exclusions:
                self.exclusions.remove(exe_path)
                self.populate_list()
                self.exclusions_changed.emit()

    def get_exclusions(self) -> List[str]:
        return self.exclusions

    def mousePressEvent(self, event: Optional[QMouseEvent]) -> None:
        if event and event.button() == Qt.MouseButton.LeftButton:
            self.drag_pos = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event: Optional[QMouseEvent]) -> None:
        if event and event.buttons() == Qt.MouseButton.LeftButton and self.drag_pos is not None:
            self.move(event.globalPosition().toPoint() - self.drag_pos)
            event.accept()


class AboutDialog(QDialog):
    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.Dialog)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setFixedSize(290, 230)
        self.drag_pos: Optional[object] = None
        self.setup_ui()

    def setup_ui(self) -> None:
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        frame = QFrame()
        frame.setStyleSheet("""
            QFrame {
                background-color: #252525;
                border: 1px solid #3c3c3c;
                border-radius: 10px;
            }
        """)
        frame_layout = QVBoxLayout(frame)
        frame_layout.setContentsMargins(14, 12, 14, 12)
        frame_layout.setSpacing(10)

        # Title bar
        title_layout = QHBoxLayout()
        title_label = QLabel("Sound Manager")
        title_label.setStyleSheet("color: #0078d7; font-weight: bold; font-size: 13px; border: none;")
        title_layout.addWidget(title_label)
        
        version_label = QLabel("v1.0")
        version_label.setStyleSheet("color: #666; font-size: 10px; border: none; margin-left: 4px;")
        title_layout.addWidget(version_label)
        title_layout.addStretch()

        close_btn = QPushButton("✕")
        close_btn.setFixedSize(20, 20)
        close_btn.clicked.connect(self.accept)
        close_btn.setStyleSheet("""
            QPushButton { color: #888; border: none; font-size: 12px; background: transparent; }
            QPushButton:hover { color: white; background: #e81123; border-radius: 3px; }
        """)
        title_layout.addWidget(close_btn)
        frame_layout.addLayout(title_layout)

        # Description text
        desc_label = QLabel(
            "A lightweight audio utility for Windows that lets you independently control and mute volume per application.\n\n"
            "• Per-application volume sliders\n"
            "• Mute/unmute toggle per app\n"
            "• Real-time volume synchronization\n"
            "• Dynamic height scaling & resizable width\n"
            "Φ Create by Digital Epoch"
        )
        desc_label.setWordWrap(True)
        desc_label.setStyleSheet("color: #CCCCCC; font-size: 10px; line-height: 1.3; border: none; background: transparent;")
        frame_layout.addWidget(desc_label, 1)

        # OK button
        ok_btn = QPushButton("OK")
        ok_btn.setFixedHeight(24)
        ok_btn.clicked.connect(self.accept)
        ok_btn.setStyleSheet("""
            QPushButton {
                background-color: #0078d7;
                color: white;
                font-weight: 500;
                font-size: 11px;
                border: none;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #1084e3;
            }
        """)
        frame_layout.addWidget(ok_btn)

        main_layout.addWidget(frame)

    def mousePressEvent(self, event: Optional[QMouseEvent]) -> None:
        if event and event.button() == Qt.MouseButton.LeftButton:
            self.drag_pos = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event: Optional[QMouseEvent]) -> None:
        if event and event.buttons() == Qt.MouseButton.LeftButton and self.drag_pos is not None:
            self.move(event.globalPosition().toPoint() - self.drag_pos)
            event.accept()

class AudioSessionWidget(QFrame):
    exclude_requested = pyqtSignal(str)
    
    def __init__(self, session, session_id: str, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.session = session
        self.session_id: str = session_id
        self.process = session.Process
        self.volume_interface = getattr(session, "SimpleAudioVolume", None) or session._ctl.QueryInterface(ISimpleAudioVolume)
        self._cached_icon: Optional[QPixmap] = None
        self._last_title: str = ""
        self._exe_path: Optional[str] = None
        
        if self.process:
            try:
                self._exe_path = self.process.exe()
            except Exception:
                pass
        
        self.setObjectName("SessionWidget")
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.setMinimumWidth(100)
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_context_menu)
        self.setup_ui()
        
        self.sync_timer = QTimer(self)
        self.sync_timer.timeout.connect(self.sync_volume_ui)
        self.sync_timer.start(SYNC_TIMER_MS)

    def setup_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 5, 10, 5)
        layout.setSpacing(2)

        top_layout = QHBoxLayout()
        self.icon_label = QLabel()
        self.icon_label.setFixedSize(24, 24)
        self.update_icon()
        top_layout.addWidget(self.icon_label)

        self.name_label = ElidedLabel("Loading...")
        self.name_label.setStyleSheet("color: #E0E0E0; font-weight: 500; font-size: 11px; background: transparent;")
        self.name_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        self.update_title()
        top_layout.addWidget(self.name_label, 1)

        self.mute_btn = QPushButton("🔊")
        self.mute_btn.setFixedSize(24, 24)
        self.mute_btn.clicked.connect(self.toggle_mute)
        self.update_mute_style()
        top_layout.addWidget(self.mute_btn)
        layout.addLayout(top_layout)

        bottom_layout = QHBoxLayout()
        self.slider = QSlider(Qt.Orientation.Horizontal)
        self.slider.setRange(0, 100)
        self.slider.setMinimumWidth(40)
        self.slider.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        try:
            if self.volume_interface:
                self.slider.setValue(int(self.volume_interface.GetMasterVolume() * 100))
        except Exception:
            pass
        self.slider.valueChanged.connect(self.set_volume)
        bottom_layout.addWidget(self.slider, 1)

        self.vol_label = QLabel(f"{self.slider.value()}%")
        self.vol_label.setFixedWidth(32)
        self.vol_label.setStyleSheet("color: #888; font-size: 10px; background: transparent;")
        bottom_layout.addWidget(self.vol_label)
        layout.addLayout(bottom_layout)

        self.setStyleSheet("""
            #SessionWidget { background-color: transparent; border: none; }
            #SessionWidget:hover { background-color: rgba(255, 255, 255, 0.05); border-radius: 4px; }
            QSlider::handle:horizontal { background: #0078d7; width: 12px; height: 12px; border-radius: 6px; margin: -4px 0; }
            QSlider::groove:horizontal { height: 4px; background: #444; border-radius: 2px; }
        """)

    def update_title(self) -> None:
        """Fetches and updates the display name/title of the process."""
        name = "System Sounds"
        if self.process:
            try:
                name = get_window_title(self.process.pid) or self.process.name()
            except Exception: 
                name = "Unknown Process"
        
        if self._last_title != name:
            self._last_title = name
            self.name_label.setText(name)

    def update_icon(self) -> None:
        if self._cached_icon is not None:
            self.icon_label.setPixmap(self._cached_icon)
            return
            
        if self.process:
            try:
                path = self.process.exe()
                if os.path.exists(path):
                    icon = QFileIconProvider().icon(QFileInfo(path))
                    self._cached_icon = icon.pixmap(24, 24)
                    self.icon_label.setPixmap(self._cached_icon)
            except Exception:
                pass

    def set_volume(self, value: int) -> None:
        if not self.volume_interface:
            return
        try:
            self.volume_interface.SetMasterVolume(value / 100.0, None)
            self.vol_label.setText(f"{value}%")
            if value > 0:
                self.volume_interface.SetMute(False, None)
            self.update_mute_style()
        except Exception:
            pass

    def toggle_mute(self) -> None:
        if not self.volume_interface:
            return
        try:
            is_muted = self.volume_interface.GetMute()
            self.volume_interface.SetMute(not is_muted, None)
            self.update_mute_style()
        except Exception:
            pass

    def sync_volume_ui(self) -> None:
        if not self.slider.isSliderDown() and self.volume_interface:
            try:
                current_vol = int(self.volume_interface.GetMasterVolume() * 100)
                if current_vol != self.slider.value():
                    self.slider.blockSignals(True)
                    self.slider.setValue(current_vol)
                    self.vol_label.setText(f"{current_vol}%")
                    self.slider.blockSignals(False)
                self.update_mute_style()
            except Exception:
                pass

    def update_mute_style(self) -> None:
        if not self.volume_interface:
            return
        try:
            is_muted = self.volume_interface.GetMute()
            self.mute_btn.setText("🔇" if is_muted else "🔊")
            color = "#ff4444" if is_muted else "#44ff44"
            self.mute_btn.setStyleSheet(f"border: none; color: {color}; font-size: 14px; background: transparent;")
        except Exception:
            pass
    
    def show_context_menu(self, position) -> None:
        """Show context menu for excluding this application."""
        if not self._exe_path:
            return
            
        menu = QMenu(self)
        menu.setStyleSheet("""
            QMenu {
                background-color: #2d2d2d;
                color: #E0E0E0;
                border: 1px solid #3c3c3c;
                border-radius: 4px;
                padding: 4px;
            }
            QMenu::item {
                padding: 6px 20px;
                border-radius: 3px;
            }
            QMenu::item:selected {
                background-color: #0078d7;
            }
        """)
        
        exclude_action = QAction("Exclude from monitoring", self)
        exclude_action.triggered.connect(lambda: self.exclude_requested.emit(self._exe_path))
        menu.addAction(exclude_action)
        
        menu.exec(self.mapToGlobal(position))
    
    def get_exe_path(self) -> Optional[str]:
        """Get the executable path for this session."""
        return self._exe_path
    
    def cleanup(self) -> None:
        """Clean up resources when widget is destroyed."""
        if hasattr(self, 'sync_timer') and self.sync_timer.isActive():
            self.sync_timer.stop()

class SoundManagerApp(QWidget):
    def __init__(self):
        super().__init__()
        icon = QIcon(str(APP_ICON_PATH)) if os.path.exists(APP_ICON_PATH) else QIcon()
        if not icon.isNull():
            self.setWindowIcon(icon)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setMouseTracking(True)
        self.setMinimumWidth(MIN_WINDOW_WIDTH_PX)
        self.setMaximumWidth(MAX_WINDOW_WIDTH_PX)

        self.drag_mode: Optional[str] = None
        self.drag_pos: Optional[object] = None
        self.drag_start_pos: Optional[object] = None
        self.drag_start_geo: Optional[object] = None
        self._session_widgets: Dict[str, AudioSessionWidget] = {}
        self._exclusions: List[str] = []
        
        self.load_exclusions()
        self.init_ui()
        self.load_settings()
        self.refresh_sessions()
        
        self.refresh_timer = QTimer(self)
        self.refresh_timer.timeout.connect(self.refresh_sessions)
        self.refresh_timer.start(REFRESH_TIMER_MS)

    def init_ui(self) -> None:
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        self.header = QFrame()
        self.header.setFixedHeight(HEADER_HEIGHT_PX)
        self.header.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.header.setStyleSheet("background-color: #252525; border-top-left-radius: 10px; border-top-right-radius: 10px;")
        h_layout = QHBoxLayout(self.header)
        h_layout.setContentsMargins(10, 0, 8, 0)
        h_layout.setSpacing(4)

        title_lbl = QLabel("Sound Manager")
        title_lbl.setStyleSheet("color: #888; font-weight: bold; font-size: 10px; text-transform: uppercase;")
        h_layout.addWidget(title_lbl)
        h_layout.addStretch()

        minimize_btn = QPushButton("—")
        minimize_btn.setFixedSize(25, 25)
        minimize_btn.setToolTip("Minimize")
        minimize_btn.clicked.connect(self.showMinimized)
        minimize_btn.setStyleSheet("QPushButton { color: #888; border: none; font-size: 12px; } QPushButton:hover { color: white; background: #3c3c3c; border-radius: 4px; }")
        h_layout.addWidget(minimize_btn)

        close_btn = QPushButton("✕")
        close_btn.setFixedSize(25, 25)
        close_btn.setToolTip("Close")
        close_btn.clicked.connect(self.close)
        close_btn.setStyleSheet("QPushButton { color: #666; border: none; font-size: 14px; } QPushButton:hover { color: white; background: #e81123; border-radius: 4px; }")
        h_layout.addWidget(close_btn)
        self.main_layout.addWidget(self.header)

        # Container inside Scroll Area
        self.container = QFrame()
        self.container.setObjectName("MainFrame")
        self.container.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        self.container.setStyleSheet("#MainFrame { background-color: rgba(30, 30, 30, 245); }")
        self.scroll_layout = QVBoxLayout(self.container)
        self.scroll_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.scroll_layout.setContentsMargins(5, 5, 5, 5)
        self.scroll_layout.setSpacing(2)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFrameShape(QFrame.Shape.NoFrame)
        self.scroll_area.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.scroll_area.setWidget(self.container)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scroll_area.setStyleSheet("""
            QScrollArea { background: transparent; border: none; }
            QScrollBar:vertical {
                background: #1e1e1e;
                width: 6px;
                margin: 0px;
                border-radius: 3px;
            }
            QScrollBar::handle:vertical {
                background: #555;
                min-height: 20px;
                border-radius: 3px;
            }
            QScrollBar::handle:vertical:hover {
                background: #777;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
        """)
        self.main_layout.addWidget(self.scroll_area)

        self.footer = QFrame()
        self.footer.setFixedHeight(FOOTER_HEIGHT_PX)
        self.footer.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.footer.setStyleSheet("background-color: #252525; border-bottom-left-radius: 10px; border-bottom-right-radius: 10px;")
        f_layout = QHBoxLayout(self.footer)
        f_layout.setContentsMargins(10, 0, 10, 0)
        
        self.status_label = QLabel("0 monitored")
        self.status_label.setStyleSheet("color: #666; font-size: 10px; font-weight: 500; background: transparent;")
        f_layout.addWidget(self.status_label)
        f_layout.addStretch()

        settings_btn = QPushButton("⚙")
        settings_btn.setFixedSize(18, 18)
        settings_btn.setToolTip("Exclusions")
        settings_btn.clicked.connect(self.show_exclusions_dialog)
        settings_btn.setStyleSheet("""
            QPushButton {
                color: #888;
                border: 1px solid #444;
                border-radius: 9px;
                font-size: 12px;
                font-weight: bold;
                background: transparent;
            }
            QPushButton:hover {
                color: white;
                border-color: #0078d7;
                background-color: #0078d7;
            }
        """)
        f_layout.addWidget(settings_btn)

        help_btn = QPushButton("?")
        help_btn.setFixedSize(18, 18)
        help_btn.setToolTip("About Sound Manager")
        help_btn.clicked.connect(self.show_about_dialog)
        help_btn.setStyleSheet("""
            QPushButton {
                color: #888;
                border: 1px solid #444;
                border-radius: 9px;
                font-size: 11px;
                font-weight: bold;
                background: transparent;
            }
            QPushButton:hover {
                color: white;
                border-color: #0078d7;
                background-color: #0078d7;
            }
        """)
        f_layout.addWidget(help_btn)
        self.main_layout.addWidget(self.footer)

        # Empty state placeholder label
        self.empty_label = QLabel("No active audio sessions")
        self.empty_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.empty_label.setStyleSheet("color: #666; font-size: 11px; font-style: italic; margin: 10px 0;")

    def _get_sessions(self) -> Optional[List]:
        try:
            return AudioUtilities.GetAllSessions()
        except Exception:
            return None

    def show_about_dialog(self) -> None:
        dialog = AboutDialog(self)
        dialog.exec()
    
    def show_exclusions_dialog(self) -> None:
        dialog = ExclusionsDialog(self._exclusions, self)
        dialog.exclusions_changed.connect(self.on_exclusions_changed)
        dialog.exec()
        self._exclusions = dialog.get_exclusions()
        self.save_exclusions()
        self.refresh_sessions()
    
    def on_exclusions_changed(self) -> None:
        """Called when exclusions are modified in the dialog."""
        pass
    
    def exclude_application(self, exe_path: str) -> None:
        """Exclude an application from monitoring."""
        if exe_path and exe_path not in self._exclusions:
            self._exclusions.append(exe_path)
            self.save_exclusions()
            self.refresh_sessions()
    
    def load_exclusions(self) -> None:
        """Load exclusions from file."""
        if os.path.exists(EXCLUSIONS_FILE):
            try:
                with open(EXCLUSIONS_FILE, 'r') as f:
                    self._exclusions = json.load(f)
            except Exception:
                self._exclusions = []
        else:
            self._exclusions = []
    
    def save_exclusions(self) -> None:
        """Save exclusions to file."""
        try:
            with open(EXCLUSIONS_FILE, 'w') as f:
                json.dump(self._exclusions, f, indent=2)
        except Exception:
            pass

    def refresh_sessions(self) -> None:
        """Updates the list of software and re-checks titles of existing software."""
        sessions = self._get_sessions()
        if sessions is None:
            if self.empty_label.parent() is None:
                self.scroll_layout.addWidget(self.empty_label)
            self.empty_label.setText("Audio service unavailable")
            self.empty_label.show()
            self.status_label.setText("Audio service unavailable")
            return

        active_sessions: Dict[str, object] = {}
        for session in sessions:
            if session.Process:
                try:
                    exe_path = session.Process.exe()
                    if exe_path in self._exclusions:
                        continue
                except Exception:
                    pass
            
            sid = get_session_id(session)
            active_sessions[sid] = session

        for sid in list(self._session_widgets.keys()):
            if sid not in active_sessions:
                widget = self._session_widgets.pop(sid)
                widget.cleanup()
                widget.setParent(None)
                widget.deleteLater()
            else:
                self._session_widgets[sid].update_title()

        for sid, session in active_sessions.items():
            if sid not in self._session_widgets:
                widget = AudioSessionWidget(session, session_id=sid)
                widget.exclude_requested.connect(self.exclude_application)
                self._session_widgets[sid] = widget
                self.scroll_layout.addWidget(widget)

        has_sessions = len(active_sessions) > 0
        if not has_sessions:
            if self.empty_label.parent() is None:
                self.scroll_layout.addWidget(self.empty_label)
            self.empty_label.setText("No active audio sessions")
            self.empty_label.show()
        else:
            if self.empty_label.parent() is not None:
                self.empty_label.setParent(None)

        count = len(active_sessions)
        excluded_count = len(self._exclusions)
        status_text = f"{count} app{'s' if count != 1 else ''} monitored"
        if excluded_count > 0:
            status_text += f" ({excluded_count} excluded)"
        self.status_label.setText(status_text)

        self.adjust_size_dynamic()

    def adjust_size_dynamic(self) -> None:
        item_count = len(self._session_widgets)

        if item_count == 0:
            calculated_height = HEADER_HEIGHT_PX + FOOTER_HEIGHT_PX + 35 + 10
        else:
            calculated_height = HEADER_HEIGHT_PX + FOOTER_HEIGHT_PX + (item_count * ITEM_HEIGHT_PX) + UI_MARGIN_PX

        screen = QApplication.primaryScreen()
        max_allowed_height = MAX_WINDOW_HEIGHT_PX
        if screen is not None:
            max_allowed_height = min(max_allowed_height, screen.availableGeometry().height() - 100)

        new_height = min(calculated_height, max_allowed_height)
        self.setFixedHeight(new_height)
        self.save_settings()

    def load_settings(self) -> None:
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, 'r') as f:
                    data = json.load(f)
                    w = max(self.minimumWidth(), min(self.maximumWidth(), data.get("width", DEFAULT_WINDOW_WIDTH_PX)))
                    self.resize(w, self.height())
                    self.move(data.get("x", 100), data.get("y", 100))
            except Exception:
                self.resize(DEFAULT_WINDOW_WIDTH_PX, self.height())
                self.snap_to_bottom_right()
        else:
            self.resize(DEFAULT_WINDOW_WIDTH_PX, self.height())
            self.snap_to_bottom_right()

    def save_settings(self) -> None:
        data = {
            "x": self.x(),
            "y": self.y(),
            "width": self.width(),
            "height": self.height()
        }
        try:
            with open(CONFIG_FILE, 'w') as f:
                json.dump(data, f)
        except Exception:
            pass

    def snap_to_bottom_right(self) -> None:
        screen = QApplication.primaryScreen()
        if screen is not None:
            geometry = screen.availableGeometry()
            self.move(geometry.width() - self.width() - 20, geometry.height() - 450)

    def _get_resize_edge(self, global_pos) -> Optional[str]:
        geo = self.frameGeometry()
        x = global_pos.x() - geo.x()
        w = geo.width()
        
        if x <= RESIZE_MARGIN_PX:
            return 'resize_left'
        elif x >= w - RESIZE_MARGIN_PX:
            return 'resize_right'
        return None

    def mousePressEvent(self, event: Optional[QMouseEvent]) -> None:
        if event is None:
            return
        if event.button() == Qt.MouseButton.LeftButton:
            global_pos = event.globalPosition().toPoint()
            edge = self._get_resize_edge(global_pos)
            if edge:
                self.drag_mode = edge
                self.drag_start_pos = global_pos
                self.drag_start_geo = self.geometry()
            else:
                self.drag_mode = 'move'
                self.drag_pos = global_pos - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event: Optional[QMouseEvent]) -> None:
        if event is None:
            return
        
        global_pos = event.globalPosition().toPoint()

        if event.buttons() == Qt.MouseButton.NoButton:
            edge = self._get_resize_edge(global_pos)
            if edge in ('resize_left', 'resize_right'):
                self.setCursor(Qt.CursorShape.SizeHorCursor)
            else:
                self.unsetCursor()
            return

        if event.buttons() == Qt.MouseButton.LeftButton:
            if self.drag_mode == 'move' and self.drag_pos is not None:
                self.move(global_pos - self.drag_pos)
                event.accept()
            elif self.drag_mode and self.drag_start_pos is not None:
                diff_x = global_pos.x() - self.drag_start_pos.x()
                geo = self.drag_start_geo
                new_x, new_y, new_w, new_h = geo.x(), geo.y(), geo.width(), geo.height()
                
                if self.drag_mode == 'resize_right':
                    new_w = max(self.minimumWidth(), min(self.maximumWidth(), geo.width() + diff_x))
                elif self.drag_mode == 'resize_left':
                    proposed_w = geo.width() - diff_x
                    if self.minimumWidth() <= proposed_w <= self.maximumWidth():
                        new_w = proposed_w
                        new_x = geo.x() + diff_x

                self.setGeometry(new_x, new_y, new_w, new_h)
                event.accept()

    def moveEvent(self, event) -> None:
        super().moveEvent(event)
        self.save_settings()

    def resizeEvent(self, event) -> None:
        super().resizeEvent(event)
        self.save_settings()

    def mouseReleaseEvent(self, event: Optional[QMouseEvent]) -> None:
        if event is None:
            return
        if event.button() == Qt.MouseButton.LeftButton:
            self.drag_mode = None
            self.save_settings()
            event.accept()
    
    def closeEvent(self, event) -> None:
        """Clean up resources when closing the application."""
        for widget in self._session_widgets.values():
            widget.cleanup()
        if hasattr(self, 'refresh_timer') and self.refresh_timer.isActive():
            self.refresh_timer.stop()
        super().closeEvent(event)

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    icon = QIcon(str(APP_ICON_PATH)) if os.path.exists(APP_ICON_PATH) else QIcon()
    if not icon.isNull():
        app.setWindowIcon(icon)

    window = SoundManagerApp()
    if not icon.isNull():
        window.setWindowIcon(icon)
    window.show()
    sys.exit(app.exec())