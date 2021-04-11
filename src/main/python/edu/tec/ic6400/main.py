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
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

# Local application imports
from src.main.python.edu.tec.ic6400.view.simplex_program_gui import MainSimplexWindow


def main():

    # Create the entire GUI program
    simplex_app = QApplication(sys.argv)
    simplex_app_window = QMainWindow()
    simplex_app_window.setGeometry(1000, 200, 600, 700)
    simplex_app_window.setWindowTitle("Calculadora Simplex")

    label_method = QtWidgets.QLabel(simplex_app_window)
    label_method.setText('Método: ')
    label_method.setFont(QtGui.QFont("Arial", 14, QtGui.QFont.Bold))
    label_method.move(100, 40)

    methods_combo = QComboBox(simplex_app_window)
    methods_combo.addItem("Seleccione un método..")
    methods_combo.addItem("Gran M")
    methods_combo.addItem("2 Fases")
    methods_combo.addItem("Dual")
    methods_combo.setGeometry(200, 150, 200, 50)
    methods_combo.move(200, 25)

    label_n_variables = QtWidgets.QLabel(simplex_app_window)
    label_n_variables.setText('Número de variables: ')
    label_n_variables.setFont(QtGui.QFont("Arial", 12, QtGui.QFont.Bold))
    label_n_variables.move(10, 55)
    label_n_variables.setGeometry(100, 85, 200, 50)

    text_n_variables = QtWidgets.QLineEdit(simplex_app_window)
    text_n_variables.move(300, 90)
    text_n_variables.resize(65, 35)
    only_int = QIntValidator()
    text_n_variables.setValidator(only_int)

    label_n_constraints = QtWidgets.QLabel(simplex_app_window)
    label_n_constraints.setText('Número de restricciones: ')
    label_n_constraints.setFont(QtGui.QFont("Arial", 12, QtGui.QFont.Bold))
    label_n_constraints.setGeometry(100, 130, 200, 50)

    text_n_constraints = QtWidgets.QLineEdit(simplex_app_window)
    text_n_constraints.move(300, 135)
    text_n_constraints.resize(65, 35)
    only_int = QIntValidator()
    text_n_constraints.setValidator(only_int)

    button_gen_model = QPushButton(simplex_app_window)
    button_gen_model.setText("Generar modelo")
    button_gen_model.setGeometry(285, 185, 150, 35)

    simplex_app_window.show()
    sys.exit(simplex_app.exec_())


main()
