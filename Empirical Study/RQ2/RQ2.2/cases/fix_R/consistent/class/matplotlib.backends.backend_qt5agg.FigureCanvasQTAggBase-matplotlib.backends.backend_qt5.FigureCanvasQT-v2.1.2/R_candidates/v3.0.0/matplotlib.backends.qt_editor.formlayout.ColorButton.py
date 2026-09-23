class ColorButton(QtWidgets.QPushButton):
    """
    Color choosing push button
    """
    colorChanged = QtCore.Signal(QtGui.QColor)

    def __init__(self, parent=None):
        QtWidgets.QPushButton.__init__(self, parent)
        self.setFixedSize(20, 20)
        self.setIconSize(QtCore.QSize(12, 12))
        self.clicked.connect(self.choose_color)
        self._color = QtGui.QColor()

    def choose_color(self):
        color = QtWidgets.QColorDialog.getColor(
            self._color, self.parentWidget(), "",
            QtWidgets.QColorDialog.ShowAlphaChannel)
        if color.isValid():
            self.set_color(color)

    def get_color(self):
        return self._color

    @QtCore.Slot(QtGui.QColor)
    def set_color(self, color):
        if color != self._color:
            self._color = color
            self.colorChanged.emit(self._color)
            pixmap = QtGui.QPixmap(self.iconSize())
            pixmap.fill(color)
            self.setIcon(QtGui.QIcon(pixmap))

    color = QtCore.Property(QtGui.QColor, get_color, set_color)
