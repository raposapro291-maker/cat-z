#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""System tray widget."""

from PyQt6.QtWidgets import QSystemTrayIcon, QMenu
from PyQt6.QtGui import QIcon, QAction
from PyQt6.QtCore import Qt, pyqtSignal, QObject


class SystemTray(QSystemTrayIcon):
    """System tray icon and menu."""
    
    show_requested = pyqtSignal()
    hide_requested = pyqtSignal()
    quit_requested = pyqtSignal()
    profile_changed = pyqtSignal(int)
    
    def __init__(self, parent=None):
        """Initialize system tray."""
        super().__init__(parent)
        self.setup_tray()
    
    def setup_tray(self) -> None:
        """Setup tray icon and menu."""
        # Create menu
        menu = QMenu()
        
        # Show/Hide action
        action_show = QAction("Mostrar", menu)
        action_show.triggered.connect(self.show_requested.emit)
        menu.addAction(action_show)
        
        menu.addSeparator()
        
        # Profiles submenu
        profiles_menu = menu.addMenu("Perfis")
        
        action_profile1 = QAction("Padrão", profiles_menu)
        action_profile1.triggered.connect(lambda: self.profile_changed.emit(1))
        profiles_menu.addAction(action_profile1)
        
        action_profile2 = QAction("Jogos", profiles_menu)
        action_profile2.triggered.connect(lambda: self.profile_changed.emit(2))
        profiles_menu.addAction(action_profile2)
        
        action_profile3 = QAction("Trabalho", profiles_menu)
        action_profile3.triggered.connect(lambda: self.profile_changed.emit(3))
        profiles_menu.addAction(action_profile3)
        
        menu.addSeparator()
        
        # Settings action
        action_settings = QAction("Configurações", menu)
        menu.addAction(action_settings)
        
        menu.addSeparator()
        
        # Quit action
        action_quit = QAction("Sair", menu)
        action_quit.triggered.connect(self.quit_requested.emit)
        menu.addAction(action_quit)
        
        self.setContextMenu(menu)
        self.activated.connect(self.on_tray_clicked)
    
    def on_tray_clicked(self, reason) -> None:
        """Handle tray icon click."""
        if reason == QSystemTrayIcon.ActivationReason.DoubleClick:
            self.show_requested.emit()
