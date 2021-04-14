"""
======================================================================
Copyright (C) 2021 Natan & Diego & Adriel
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.
    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.

    Instituto Tecnologico de Costa Rica
    Investigación de Operaciones - IC-6400
    Simplex Method
    Disponible en: https://github.com/natanfdecastro/simplex-method-ic-6400
    Natan Fernandez de Castro - 2017105774
    Diego Acuña Cerdas - 2018109507
    Adriel Casco Parker - 2016254510
========================================================================
"""

# Standard library imports
import sys
import os

# Third party imports
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.uic.Compiler.qtproxies import QtWidgets, QtGui
from PyQt5.QtWidgets import (
    QApplication,
    QComboBox,
    QFormLayout,
    QLineEdit,
    QStackedLayout,
    QVBoxLayout,
    QWidget,
)

# Local application imports

# Global Variables, constants and macros
GREATER_EQUAL_SIGN = u"\u2264"  # code for <=
LESS_EQUAL_SIGN = u"\u2265"   # code for >=
EQUAL_SIGN = "="  # char for =


class SimplexProgramGui(QWidget):

    def __init__(self):

        # Simplex main window properties
        super().__init__()

        self.setWindowTitle("MENAlex Method Calculator")
        # self.setStyleSheet("background-color: #000a12; color: white")
        # self.resize(1200, 600)
        self.items = []
        self.item_count = 0

        # start the gui
        self.set_simplex_main_window()
        # self.set_simplex_main_layout()

        # set main window behaviour
        self.setFixedWidth(self.sizeHint().width()+100)
        self.setWindowFlags(Qt.WindowCloseButtonHint | Qt.WindowMinimizeButtonHint)

    def set_simplex_main_window(self):

        self.outer_layout = QVBoxLayout()

        # title_label = QtWidgets.QLabel("MENALEX METHOD CALCULATOR", self)
        # title_label.setFont(QtGui.QFont("Consolas", 18, QtGui.QFont.Bold))
        # outer_layout.addWidget(title_label)
        # title_label.move(15, 20)

        self.method_combo_box = QComboBox()
        self.method_combo_box.addItems(["Big M Method", "Dual Method", "Two Phases Method"])
        self.method_combo_box.activated.connect(self.switch_page)

        self.stacked_layout = QStackedLayout()

        # Big M Page
        self.big_m_method_page = QWidget()
        self.big_m_method_page_layout = QFormLayout()
        self.big_m_method_page_layout.addRow("Number of Variables: ", QLineEdit())
        self.big_m_method_page_layout.addRow("Number of Restrictions: ", QLineEdit())

        # Dropdown for maximize and minimize
        self.big_m_combo_page_layout = QComboBox()
        self.big_m_combo_page_layout.addItems(["Maximize", "Minimize"])
        self.big_m_method_page_layout.addWidget(self.big_m_combo_page_layout)

        # Checkbox for .txt file generation
        self.big_m_method_page_layout.addWidget(QCheckBox("Generate .txt solution file"))

        self.big_m_method_page.setLayout(self.big_m_method_page_layout)
        self.stacked_layout.addWidget(self.big_m_method_page)

        # End of BM page

        # Dual Method Page
        self.dual_method_page = QWidget()
        self.dual_method_page_layout = QFormLayout()

        # Textboxs for variables and restrictions
        self.dual_method_page_layout.addRow("Number of Variables Dual: ", QLineEdit())
        self.dual_method_page_layout.addRow("Number of Restrictions: ", QLineEdit())

        # Dropdown for maximize and minimize
        self.dual_method_combo_page_layout = QComboBox()
        self.dual_method_combo_page_layout.addItems(["Maximize", "Minimize"])
        self.dual_method_page_layout.addWidget(self.dual_method_combo_page_layout)

        # Checkbox for .txt file generation
        self.dual_method_page_layout.addWidget(QCheckBox("Generate .txt solution file"))

        self.dual_method_page.setLayout(self.dual_method_page_layout)
        self.stacked_layout.addWidget(self.dual_method_page)

        # End of DM page

        # Two Phases Method
        self.two_phases_method_page = QWidget()
        self.two_phases_method_page_layout = QFormLayout()
        self.two_phases_method_page_layout.addRow("Number of Variables 2P: ", QLineEdit())
        self.two_phases_method_page_layout.addRow("Number of Restrictions: ", QLineEdit())

        # Dropdown for maximize and minimize
        self.two_phases_method_combo_page_layout = QComboBox()
        self.two_phases_method_combo_page_layout.addItems(["Maximize", "Minimize"])
        self.two_phases_method_page_layout.addWidget(self.two_phases_method_combo_page_layout)

        # Checkbox for .txt file generation
        self.two_phases_method_page_layout.addWidget(QCheckBox("Generate .txt solution file"))

        self.two_phases_method_page.setLayout(self.two_phases_method_page_layout)
        self.stacked_layout.addWidget(self.two_phases_method_page)

        # End of 2PM page

        self.outer_layout.addWidget(self.method_combo_box)

        self.outer_layout.addLayout(self.stacked_layout)

        self.setLayout(self.outer_layout)

    def switch_page(self):
        self.stacked_layout.setCurrentIndex(self.method_combo_box.currentIndex())


if __name__ == "__main__":

    simplex_app = QApplication([])
    simplex_main_window = SimplexProgramGui()
    simplex_main_window.show()
    sys.exit(simplex_app.exec_())
