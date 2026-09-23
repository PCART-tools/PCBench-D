    def __init__(self, color, parent=None):
        super().__init__()
        assert isinstance(color, QtGui.QColor)
        self.lineedit = QtWidgets.QLineEdit(
            mcolors.to_hex(color.getRgbF(), keep_alpha=True), parent)
        self.lineedit.editingFinished.connect(self.update_color)
        self.addWidget(self.lineedit)
        self.colorbtn = ColorButton(parent)
        self.colorbtn.color = color
        self.colorbtn.colorChanged.connect(self.update_text)
        self.addWidget(self.colorbtn)
