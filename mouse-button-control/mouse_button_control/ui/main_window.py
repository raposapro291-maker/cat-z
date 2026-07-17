"""Main application window."""

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QTabWidget, QMessageBox,
)
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt, pyqtSignal
from pathlib import Path


class MainWindow(QMainWindow):
    """Main application window."""

    closed = pyqtSignal()

    def __init__(self, config_manager=None):
        """Initialize main window."""
        super().__init__()
        self.config_manager = config_manager
        self.setup_ui()
        self.apply_styles()

    def setup_ui(self) -> None:
        """Setup user interface."""
        self.setWindowTitle("Mouse Button Control for Linux")
        self.setGeometry(100, 100, 1200, 700)
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout(central_widget)
        
        # Tab widget
        self.tabs = QTabWidget()
        layout.addWidget(self.tabs)
        
        # Add tabs
        self._add_tabs()
        
        central_widget.setLayout(layout)

    def _add_tabs(self) -> None:
        """Add tabs to the interface."""
        # Placeholder tabs
        from PyQt6.QtWidgets import QLabel
        
        tab_names = [
            "Perfis",
            "Botões",
            "Macros",
            "Teclado",
            "Automação",
            "Configurações",
            "Logs",
        ]
        
        for tab_name in tab_names:
            label = QLabel(f"Aba {tab_name} - Em desenvolvimento")
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.tabs.addTab(label, tab_name)

    def apply_styles(self) -> None:
        """Apply application styles."""
        # Dark theme stylesheet
        stylesheet = """
            QMainWindow {
                background-color: #1e1e1e;
            }
            QTabWidget::pane {
                border: 1px solid #3d3d3d;
            }
            QTabBar::tab {
                background-color: #2d2d2d;
                color: #ffffff;
                padding: 8px 20px;
                border: 1px solid #3d3d3d;
            }
            QTabBar::tab:selected {
                background-color: #0d47a1;
                color: #ffffff;
            }
            QLabel {
                color: #ffffff;
            }
        """
        self.setStyleSheet(stylesheet)

    def closeEvent(self, event) -> None:
        """Handle window close event."""
        reply = QMessageBox.question(
            self, "Fechar", "Deseja realmente fechar?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            self.closed.emit()
            event.accept()
        else:
            event.ignore()
