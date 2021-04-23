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
import sympy
import numpy as np  # cambiar nombre de referencia

# Third party imports
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication,
    QComboBox,
    QVBoxLayout,
    QWidget,
)
from qt_material import apply_stylesheet

# Local application imports
from src.main.python.edu.tec.ic6400.controller.big_m_method import *
from src.main.python.edu.tec.ic6400.controller.dual_method import *
from src.main.python.edu.tec.ic6400.controller.two_phases_method import *

# from src.main.python.edu.tec.ic6400.model.txt_method_writer import *

# Global Variables, constants and macros
GREATER_EQUAL_SIGN = u"\u2264"  # code for <=
LESS_EQUAL_SIGN = u"\u2265"  # code for >=
EQUAL_SIGN = "="  # char for =
HEADER_SPACE = 11


class SimplexProgramGui(QMainWindow):

    def __init__(self):

        # Extend the functionality of the Class method
        super(SimplexProgramGui, self).__init__()

        # Simplex main window properties
        self.setWindowTitle("MENAlex Method Calculator")
        self.setStyleSheet("background-color: #000a12; font-family: Consolas; color: white")

        # Quitar y agregar en combo_box directamente con las variables globales
        self.CONSTRAINT_EQUALITY_SIGNS = [u"\u2264", u"\u2265", "="]  # you can choose either <=,>=,= for constraint
        self.column_items_count = 2
        self.row_items_count = 2

        #
        self.objective_function_label = QLabel("Objective function", self)
        self.objective_function_label.setFont(QFont('Consolas', 16))
        # self.objective_function_label.setFixedHeight(self.objective_function_label.sizeHint().height())
        # El tercer parámetro pasarlo como un QLabel no con un arreglo de ComboBox
        self.objective_fxn_table = self.create_table(1, 4, ["="], self.create_header_labels(2))

        # Buscar que la entrada sea siempre Uppercase
        z_item = QTableWidgetItem("U")
        self.objective_fxn_table.setItem(0, 3, z_item)

        # make the objective fxn table's size fit perfectly with the rows
        # Buscar en docu
        self.objective_fxn_table.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.objective_fxn_table.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        #
        # self.objective_fxn_table.resizeColumnsToContents()
        # Buscar docu
        self.objective_fxn_table.setFixedHeight(
            self.objective_fxn_table.verticalHeader().length() +
            self.objective_fxn_table.horizontalHeader().height() + 13)

        self.constraints_label = QLabel("Constraints", self)
        self.constraints_label.setFont(QFont('Consolas', 16))
        self.constraints_label.setFixedHeight(self.constraints_label.sizeHint().height())
        self.constraint_table = self.create_table(2, 4, self.CONSTRAINT_EQUALITY_SIGNS, self.create_header_labels(2))
        self.constraint_table.setFixedHeight(self.constraint_table.sizeHint().height())

        # self.objective_fxn_table.setRowHeight(0, 11)  # Set the height of the fourth row of the table
        # texto para solución
        self.answers_label = QLabel()

        self.variables_number_label = QLabel('Number of Variables: ', self)
        self.variables_number_spin = QSpinBox(self)
        self.variables_number_spin.setRange(2, 17)
        self.variables_number_spin.valueChanged.connect(self.compare_value_changed_column)

        self.restrictions_number_label = QLabel('Number of Restrictions: ', self)
        self.restrictions_number_spin = QSpinBox(self)
        self.restrictions_number_spin.setRange(2, 17)
        self.restrictions_number_spin.valueChanged.connect(self.compare_value_changed_row)

        self.solve_btn = QPushButton('Solve', self)

        self.method_combo_box = QComboBox()
        for item in ["Big M Method", "Dual Method", "Two Phases Method"]:
            self.method_combo_box.addItem(item)

        self.max_min_combo_box = QComboBox()
        for item in ["Maximize", "Minimize"]:
            self.max_min_combo_box.addItem(item)

        self.txt_generation_check_box = QCheckBox("Generate .txt solution file")

        self.solve_btn.clicked.connect(self.solve_method)

        # Set the layout (draw it)

        vbox_layout1 = QHBoxLayout(self)
        self.vbox_layout2 = QVBoxLayout(self)

        vbox_layout1.addWidget(self.variables_number_label)
        vbox_layout1.addWidget(self.variables_number_spin)
        vbox_layout1.addWidget(self.restrictions_number_label)
        vbox_layout1.addWidget(self.restrictions_number_spin)
        vbox_layout1.addWidget(self.method_combo_box)
        vbox_layout1.addWidget(self.max_min_combo_box)
        vbox_layout1.addWidget(self.txt_generation_check_box)
        vbox_layout1.addWidget(self.solve_btn)

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        main_v_layout = QVBoxLayout(self)
        central_widget.setLayout(main_v_layout)

        self.vbox_layout2.addWidget(self.objective_function_label)
        self.vbox_layout2.addWidget(self.objective_fxn_table)
        self.vbox_layout2.addWidget(self.constraints_label)
        self.vbox_layout2.addWidget(self.constraint_table)
        self.vbox_layout2.addWidget(self.answers_label)

        main_v_layout.addLayout(vbox_layout1)
        main_v_layout.addLayout(self.vbox_layout2)

    def compare_value_changed_column(self, new_column_count: int):

        for ii in range(self.column_items_count, new_column_count):
            self.add_column_event()
        for ii in range(new_column_count, self.column_items_count):
            self.del_col_event()
        self.column_items_count = new_column_count

    def compare_value_changed_row(self, new_row_count: int):

        for ii in range(self.row_items_count, new_row_count):
            self.add_row_event()
        for ii in range(new_row_count, self.row_items_count):
            self.del_row_event()
        self.row_items_count = new_row_count

    def create_table(self, rows, cols, equality_signs=None, horizontal_headers=None, vertical_headers=None):
        table = QTableWidget(self)
        table.setColumnCount(cols)
        table.setRowCount(rows)

        # Set the table headers
        if horizontal_headers:
            table.setHorizontalHeaderLabels(horizontal_headers)

        if vertical_headers:
            table.setVerticalHeaderLabels(vertical_headers)

        # add <=,>=,= signs so that person can select the whether that constraint is <=,>= or =
        # its also used for the objective fxn but in the objective fxn we just use = Z so an [=] sign is passed
        # for equality signs in the creation of the objective fxn table in the create_ui function
        if equality_signs:
            numofrows = table.rowCount()
            numofcols = table.columnCount()
            # add combo items to self.constraint_table
            for index in range(numofrows):
                equality_signs_combo = QComboBox()
                for item in equality_signs:
                    equality_signs_combo.addItem(item)
                table.setCellWidget(index, numofcols - 2, equality_signs_combo)

        return table

    @staticmethod
    def create_header_labels(num_of_variables):
        """Name the columns for the tables x1,x2,.... give a space and then add bi"""
        header_labels = [" " * HEADER_SPACE + "x" + str(i + 1) + " " * HEADER_SPACE for i in range(num_of_variables)]
        header_labels.extend([" " * HEADER_SPACE, " " * HEADER_SPACE + "LD" + " " * HEADER_SPACE])
        return header_labels

    def del_row_event(self):
        # allow a maximum of one constraint
        if self.constraint_table.rowCount() > 1:
            self.constraint_table.removeRow(self.constraint_table.rowCount() - 1)

    def del_col_event(self):
        # if we have x1,x2 and the signs and bi column don't allow deletion of column, else delete
        if self.constraint_table.columnCount() > 4:
            self.constraint_table.removeColumn(self.constraint_table.columnCount() - 3)
            self.objective_fxn_table.removeColumn(self.objective_fxn_table.columnCount() - 3)

    def add_column_event(self):
        self.constraint_table.insertColumn(self.constraint_table.columnCount() - 2)
        self.objective_fxn_table.insertColumn(self.objective_fxn_table.columnCount() - 2)
        self.constraint_table.setHorizontalHeaderLabels(
            self.create_header_labels(self.constraint_table.columnCount() - 2))
        self.objective_fxn_table.setHorizontalHeaderLabels(
            self.create_header_labels(self.constraint_table.columnCount() - 2))

        # make the objective fxn table's size fit perfectly with the rows and columns
        self.objective_fxn_table.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.objective_fxn_table.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.objective_fxn_table.setFixedHeight(
            self.objective_fxn_table.verticalHeader().length() + self.objective_fxn_table.horizontalHeader().height())

    def add_row_event(self):
        self.constraint_table.insertRow(self.constraint_table.rowCount())
        equality_signs_combo = QComboBox()
        for item in self.CONSTRAINT_EQUALITY_SIGNS:
            equality_signs_combo.addItem(item)
        self.constraint_table.setCellWidget(self.constraint_table.rowCount() - 1,
                                            self.constraint_table.columnCount() - 2, equality_signs_combo)
        self.constraint_table.resizeRowsToContents()

    def solve_method(self):

        method_to_solve = self.method_combo_box.currentText().lower()
        max_min_operation_to_use = self.max_min_combo_box.currentText().lower()

        # Get the data entered in tables from the main simplex window
        objective_function = self.get_obj_fxn()
        restriction_matrix = self.form_unaugmented_matrix()
        restriction_signs = self.read_equality_signs(self.constraint_table.columnCount() - 2,
                                                     self.constraint_table)

        # Check the method entered to solve and call the respective module
        if method_to_solve == "big m method":
            if self.txt_generation_check_box.isChecked():
                big_m_method(max_min_operation_to_use, True)
            else:
                big_m_method(max_min_operation_to_use, False)
        elif method_to_solve == "dual method":

            if self.txt_generation_check_box.isChecked():
                dual_method(max_min_operation_to_use, True, objective_function, restriction_matrix, restriction_signs)
            else:
                dual_method(max_min_operation_to_use, False, objective_function, restriction_matrix, restriction_signs)
        else:
            if self.txt_generation_check_box.isChecked():
                self.answers_label.setText(two_phases_method(max_min_operation_to_use, True, objective_function, restriction_matrix, restriction_signs))
            else:
                self.answers_label.setText(two_phases_method(max_min_operation_to_use, False, objective_function, restriction_matrix, restriction_signs))

    @staticmethod
    def read_table_items(table, start_row, end_row, start_col, end_col):
        read_table = np.zeros((end_row - start_row, end_col - start_col), dtype=sympy.Symbol)
        for i in range(start_row, end_row):
            for j in range(start_col, end_col):
                read_table[i - end_row][j - end_col] = float(table.item(i, j).text())

        return read_table

    @staticmethod
    def read_equality_signs(equality_signs_column, table):
        equality_signs = []
        for i in range(table.rowCount()):
            equality_signs.append(table.cellWidget(i, equality_signs_column).currentText())
        return equality_signs

    def form_unaugmented_matrix(self):
        obj_fxn = self.get_obj_fxn()
        split1_of_constraints = self.read_table_items(self.constraint_table, 0, self.constraint_table.rowCount(), 0,
                                                      self.constraint_table.columnCount() - 2)
        split2_of_constraints = self.read_table_items(self.constraint_table, 0, self.constraint_table.rowCount(),
                                                      self.constraint_table.columnCount() - 1,
                                                      self.constraint_table.columnCount())
        unaugmented_matrix_without_obj_fxn = np.concatenate((np.array(split2_of_constraints), split1_of_constraints),
                                                            axis=1)
        unaugmented_matrix = np.vstack((obj_fxn, unaugmented_matrix_without_obj_fxn))
        return unaugmented_matrix

    def get_obj_fxn(self):
        obj_fxn_coeff = self.read_table_items(self.objective_fxn_table, 0, self.objective_fxn_table.rowCount(), 0,
                                              self.objective_fxn_table.columnCount() - 2)
        obj_fxn = np.insert(obj_fxn_coeff, 0, 0)
        return obj_fxn


if __name__ == "__main__":
    simplex_app = QApplication(sys.argv)
    simplex_main_window = SimplexProgramGui()
    #apply_stylesheet(simplex_app, theme='dark_cyan.xml')
    simplex_main_window.show()
    sys.exit(simplex_app.exec())
