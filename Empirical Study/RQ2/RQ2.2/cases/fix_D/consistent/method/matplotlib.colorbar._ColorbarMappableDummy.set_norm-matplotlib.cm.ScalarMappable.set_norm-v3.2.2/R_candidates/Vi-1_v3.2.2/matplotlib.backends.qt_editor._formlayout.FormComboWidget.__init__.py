    def __init__(self, datalist, comment="", parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        layout = QtWidgets.QVBoxLayout()
        self.setLayout(layout)
        self.combobox = QtWidgets.QComboBox()
        layout.addWidget(self.combobox)

        self.stackwidget = QtWidgets.QStackedWidget(self)
        layout.addWidget(self.stackwidget)
        self.combobox.currentIndexChanged.connect(
            self.stackwidget.setCurrentIndex)

        self.widgetlist = []
        for data, title, comment in datalist:
            self.combobox.addItem(title)
            widget = FormWidget(data, comment=comment, parent=self)
            self.stackwidget.addWidget(widget)
            self.widgetlist.append(widget)
