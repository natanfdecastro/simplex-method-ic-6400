

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QIntValidator
from PyQt5.QtWidgets import QApplication, QMainWindow, QComboBox, QPushButton
import sys

def window():
    app=QApplication(sys.argv)
    win=QMainWindow()
    win.setGeometry(1000,200,600,700)
    win.setWindowTitle("Calculadora Simplex")


    label_method = QtWidgets.QLabel(win)
    label_method.setText('Método: ')
    label_method.setFont(QtGui.QFont("Arial", 14, QtGui.QFont.Bold))
    label_method.move(100, 40)

    methods_combo = QComboBox(win)
    methods_combo.addItem("Seleccione un método..")
    methods_combo.addItem("Gran M")
    methods_combo.addItem("2 Fases")
    methods_combo.addItem("Dual")
    methods_combo.setGeometry(200, 150, 200, 50)
    methods_combo.move(200, 25)

    label_n_variables = QtWidgets.QLabel(win)
    label_n_variables.setText('Número de variables: ')
    label_n_variables.setFont(QtGui.QFont("Arial", 12, QtGui.QFont.Bold))
    label_n_variables.move(10, 55)
    label_n_variables.setGeometry(100, 85, 200, 50)

    text_n_variables=QtWidgets.QLineEdit(win)
    text_n_variables.move(300, 90)
    text_n_variables.resize(65, 35)
    only_int = QIntValidator()
    text_n_variables.setValidator(only_int)

    label_n_constraints = QtWidgets.QLabel(win)
    label_n_constraints.setText('Número de restricciones: ')
    label_n_constraints.setFont(QtGui.QFont("Arial", 12, QtGui.QFont.Bold))
    label_n_constraints.setGeometry(100, 130, 200, 50)

    text_n_constraints = QtWidgets.QLineEdit(win)
    text_n_constraints.move(300, 135)
    text_n_constraints.resize(65, 35)
    only_int = QIntValidator()
    text_n_constraints.setValidator(only_int)

    button_gen_model = QPushButton(win)
    button_gen_model.setText("Generar modelo")
    button_gen_model.setGeometry(285, 185, 150, 35)




    win.show()
    sys.exit(app.exec_())

window()



