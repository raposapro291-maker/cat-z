#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Profiles tab implementation."""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget,
    QTableWidgetItem, QMessageBox, QDialog, QLabel, QLineEdit,
    QComboBox, QTextEdit, QFormLayout
)
from PyQt6.QtCore import Qt, pyqtSignal


class ProfilesTab(QWidget):
    """Profiles management tab."""
    
    profile_changed = pyqtSignal(int)
    
    def __init__(self, config_manager=None):
        """Initialize profiles tab."""
        super().__init__()
        self.config_manager = config_manager
        self.setup_ui()
        self.load_profiles()
    
    def setup_ui(self) -> None:
        """Setup tab interface."""
        layout = QVBoxLayout()
        
        # Buttons layout
        buttons_layout = QHBoxLayout()
        
        btn_new = QPushButton("Novo Perfil")
        btn_new.clicked.connect(self.create_profile)
        buttons_layout.addWidget(btn_new)
        
        btn_edit = QPushButton("Editar")
        btn_edit.clicked.connect(self.edit_profile)
        buttons_layout.addWidget(btn_edit)
        
        btn_duplicate = QPushButton("Duplicar")
        btn_duplicate.clicked.connect(self.duplicate_profile)
        buttons_layout.addWidget(btn_duplicate)
        
        btn_delete = QPushButton("Excluir")
        btn_delete.clicked.connect(self.delete_profile)
        buttons_layout.addWidget(btn_delete)
        
        buttons_layout.addStretch()
        
        btn_export = QPushButton("Exportar")
        btn_export.clicked.connect(self.export_profile)
        buttons_layout.addWidget(btn_export)
        
        btn_import = QPushButton("Importar")
        btn_import.clicked.connect(self.import_profile)
        buttons_layout.addWidget(btn_import)
        
        layout.addLayout(buttons_layout)
        
        # Profiles table
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Nome", "Tipo", "Status", "Açoes"])
        self.table.itemClicked.connect(self.on_profile_selected)
        layout.addWidget(self.table)
        
        self.setLayout(layout)
    
    def load_profiles(self) -> None:
        """Load profiles from config."""
        if not self.config_manager:
            return
        
        profiles = self.config_manager.get_all_profiles()
        self.table.setRowCount(len(profiles))
        
        for row, profile in enumerate(profiles):
            self.table.setItem(row, 0, QTableWidgetItem(profile.get("name", "")))
            self.table.setItem(row, 1, QTableWidgetItem(profile.get("type", "")))
            status = "Ativo" if profile.get("active") else "Inativo"
            self.table.setItem(row, 2, QTableWidgetItem(status))
    
    def create_profile(self) -> None:
        """Create new profile."""
        dialog = ProfileDialog()
        if dialog.exec() == QDialog.DialogCode.Accepted:
            profile_data = dialog.get_data()
            if self.config_manager:
                profile_id = self.config_manager.save_profile(profile_data)
                if profile_id:
                    QMessageBox.information(self, "Sucesso", "Perfil criado com sucesso!")
                    self.load_profiles()
    
    def edit_profile(self) -> None:
        """Edit selected profile."""
        current_row = self.table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "Aviso", "Selecione um perfil para editar")
            return
        
        profile_name = self.table.item(current_row, 0).text()
        QMessageBox.information(self, "Info", f"Editando: {profile_name}")
    
    def duplicate_profile(self) -> None:
        """Duplicate selected profile."""
        current_row = self.table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "Aviso", "Selecione um perfil para duplicar")
            return
        
        profile_name = self.table.item(current_row, 0).text()
        QMessageBox.information(self, "Info", f"Duplicando: {profile_name}")
    
    def delete_profile(self) -> None:
        """Delete selected profile."""
        current_row = self.table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "Aviso", "Selecione um perfil para excluir")
            return
        
        profile_name = self.table.item(current_row, 0).text()
        reply = QMessageBox.question(
            self, "Confirmar",
            f"Deseja excluir o perfil '{profile_name}'?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            QMessageBox.information(self, "Info", f"Excluído: {profile_name}")
            self.load_profiles()
    
    def export_profile(self) -> None:
        """Export selected profile."""
        current_row = self.table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "Aviso", "Selecione um perfil para exportar")
            return
        
        profile_name = self.table.item(current_row, 0).text()
        QMessageBox.information(self, "Info", f"Exportando: {profile_name}")
    
    def import_profile(self) -> None:
        """Import profile from file."""
        QMessageBox.information(self, "Info", "Importar perfil")
    
    def on_profile_selected(self, item) -> None:
        """Handle profile selection."""
        pass


class ProfileDialog(QDialog):
    """Dialog for creating/editing profiles."""
    
    def __init__(self, profile_data=None):
        """Initialize dialog."""
        super().__init__()
        self.profile_data = profile_data or {}
        self.setup_ui()
    
    def setup_ui(self) -> None:
        """Setup dialog interface."""
        self.setWindowTitle("Novo Perfil")
        self.setGeometry(200, 200, 400, 300)
        
        layout = QFormLayout()
        
        # Name
        self.name_input = QLineEdit()
        self.name_input.setText(self.profile_data.get("name", ""))
        layout.addRow("Nome:", self.name_input)
        
        # Type
        self.type_combo = QComboBox()
        self.type_combo.addItems(["default", "gaming", "work", "custom"])
        layout.addRow("Tipo:", self.type_combo)
        
        # Description
        self.desc_input = QTextEdit()
        self.desc_input.setText(self.profile_data.get("description", ""))
        layout.addRow("Descrição:", self.desc_input)
        
        # Buttons
        buttons_layout = QHBoxLayout()
        
        btn_ok = QPushButton("OK")
        btn_ok.clicked.connect(self.accept)
        buttons_layout.addWidget(btn_ok)
        
        btn_cancel = QPushButton("Cancelar")
        btn_cancel.clicked.connect(self.reject)
        buttons_layout.addWidget(btn_cancel)
        
        layout.addRow("", buttons_layout)
        self.setLayout(layout)
    
    def get_data(self) -> dict:
        """Get dialog data."""
        return {
            "name": self.name_input.text(),
            "type": self.type_combo.currentText(),
            "description": self.desc_input.toPlainText(),
        }
