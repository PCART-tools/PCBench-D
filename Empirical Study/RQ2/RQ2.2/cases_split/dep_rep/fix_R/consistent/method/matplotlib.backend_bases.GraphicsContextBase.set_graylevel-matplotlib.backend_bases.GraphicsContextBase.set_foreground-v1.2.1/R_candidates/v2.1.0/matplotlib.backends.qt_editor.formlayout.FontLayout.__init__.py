    def __init__(self, value, parent=None):
        QtWidgets.QGridLayout.__init__(self)
        font = tuple_to_qfont(value)
        assert font is not None

        # Font family
        self.family = QtWidgets.QFontComboBox(parent)
        self.family.setCurrentFont(font)
        self.addWidget(self.family, 0, 0, 1, -1)

        # Font size
        self.size = QtWidgets.QComboBox(parent)
        self.size.setEditable(True)
        sizelist = list(range(6, 12)) + list(range(12, 30, 2)) + [36, 48, 72]
        size = font.pointSize()
        if size not in sizelist:
            sizelist.append(size)
            sizelist.sort()
        self.size.addItems([str(s) for s in sizelist])
        self.size.setCurrentIndex(sizelist.index(size))
        self.addWidget(self.size, 1, 0)

        # Italic or not
        self.italic = QtWidgets.QCheckBox(self.tr("Italic"), parent)
        self.italic.setChecked(font.italic())
        self.addWidget(self.italic, 1, 1)

        # Bold or not
        self.bold = QtWidgets.QCheckBox(self.tr("Bold"), parent)
        self.bold.setChecked(font.bold())
        self.addWidget(self.bold, 1, 2)
