#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Main entry point for Mouse Button Control."""

import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt

from config.config_manager import ConfigManager
from device.device_manager import DeviceManager
from device.device_listener import DeviceListener
from macro.macro_engine import MacroEngine
from automation.profile_switcher import ProfileSwitcher
from ui.main_window import MainWindow
from utils.logger import Logger


class Application:
    """Main application class."""

    def __init__(self):
        """Initialize application."""
        self.logger = Logger.get_logger()
        self.config = ConfigManager()
        self.device_manager = DeviceManager()
        self.device_listener = DeviceListener()
        self.macro_engine = MacroEngine()
        self.profile_switcher = ProfileSwitcher(self.config)
        self.app = QApplication(sys.argv)
        self.main_window = None

    def initialize(self) -> None:
        """Initialize application components."""
        self.logger.info("Inicializando aplicação...")
        
        # Create default profiles if needed
        self.config.create_default_profiles()
        
        # Setup device monitoring
        self.device_manager.start_monitoring()
        
        # Setup profile auto-switching
        if self.config.get("auto_profile_switch", True):
            self.profile_switcher.start_monitoring()
        
        # Setup device listener
        self.device_listener.start()
        
        self.logger.info("Aplicação inicializada com sucesso!")

    def run(self) -> int:
        """Run the application."""
        try:
            self.initialize()
            
            # Create main window
            self.main_window = MainWindow(self.config)
            self.main_window.closed.connect(self.cleanup)
            self.main_window.show()
            
            self.logger.info("Janela principal exibida")
            
            return self.app.exec()
        except Exception as e:
            self.logger.error(f"Erro ao executar aplicação: {e}", exc_info=True)
            return 1

    def cleanup(self) -> None:
        """Cleanup resources."""
        self.logger.info("Encerrando aplicação...")
        
        try:
            self.device_listener.stop()
            self.device_manager.stop_monitoring()
            self.profile_switcher.stop_monitoring()
            self.config.backup_config()
            
            self.logger.info("Aplicação encerrada com sucesso!")
        except Exception as e:
            self.logger.error(f"Erro ao encerrar: {e}", exc_info=True)


def main() -> int:
    """Main entry point."""
    app = Application()
    return app.run()


if __name__ == "__main__":
    sys.exit(main())
