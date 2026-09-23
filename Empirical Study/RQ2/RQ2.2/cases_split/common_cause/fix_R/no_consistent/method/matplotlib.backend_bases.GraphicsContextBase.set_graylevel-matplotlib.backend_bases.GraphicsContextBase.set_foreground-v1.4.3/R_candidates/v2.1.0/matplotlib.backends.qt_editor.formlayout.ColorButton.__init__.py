    def __init__(self, parent=None):
        QtWidgets.QPushButton.__init__(self, parent)
        self.setFixedSize(20, 20)
        self.setIconSize(QtCore.QSize(12, 12))
        self.clicked.connect(self.choose_color)
        self._color = QtGui.QColor()
