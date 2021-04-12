from PyQt5 import QtWidgets


class Widget(QtWidgets.QWidget):

    def __init__(self, *args, **kwargs):
        super().__init__()
        self.resize(300, 300)
        self.items = []
        self.item_count = 0

        label = QtWidgets.QLabel("NUMBER OF LINE EDITS")

        self.spinBox = QtWidgets.QSpinBox(self)
        self.spinBox.setRange(0, 7)
        self.spinBox.valueChanged.connect(self.set_item_count)

        button = QtWidgets.QPushButton("apply", clicked=self.on_clicked)

        self.lineEdit = QtWidgets.QLineEdit

        groupBox = QtWidgets.QGroupBox("Line Edit")
        self.item_layout = QtWidgets.QVBoxLayout(groupBox)
        self.item_layout.addStretch(2)

        g_layout = QtWidgets.QGridLayout(self)
        g_layout.addWidget(label, 0, 0, 1, 2)
        g_layout.addWidget(self.spinBox, 0, 2, 1, 1)
        g_layout.addWidget(button, 1, 0, 1, 1)
        g_layout.addWidget(groupBox, 2, 0, 5, 3)

    def on_clicked(self):
        print(*[item.text() for item in self.items[:self.spinBox.value()]], sep="\n")

    def set_item_count(self, new_count: int):
        n_items = len(self.items)
        for ii in range(n_items, new_count):
            item = self.lineEdit(self)
            self.items.append(item)
            self.item_layout.insertWidget(n_items, item)
        for ii in range(self.item_count, new_count):
            self.item_layout.itemAt(ii).widget().show()
        for ii in range(new_count, self.item_count):
            self.item_layout.itemAt(ii).widget().hide()
        self.item_count = new_count


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = Widget()
    window.show()
    app.exec()
