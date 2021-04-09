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
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QWidget

# Local application imports


def show_window():
    app = QApplication(sys.argv)
    q_main_window = QWidget()
    q_main_window.setGeometry(200, 200, 600, 300)
    q_main_window.setWindowTitle("Simplex Method")
    q_main_window.move(200, 200)
    message = QLabel('<h1>Simplex Method Calculator</h1>', parent=q_main_window)
    message.move(60, 15)

    q_main_window.show()
    sys.exit(app.exec_())
