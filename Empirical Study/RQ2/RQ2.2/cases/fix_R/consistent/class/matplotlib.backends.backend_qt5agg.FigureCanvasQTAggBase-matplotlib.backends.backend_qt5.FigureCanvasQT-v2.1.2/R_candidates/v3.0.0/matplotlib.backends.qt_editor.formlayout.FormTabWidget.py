class FormTabWidget(QtWidgets.QWidget):
    update_buttons = QtCore.Signal()

    def __init__(self, datalist, comment="", parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        layout = QtWidgets.QVBoxLayout()
        self.tabwidget = QtWidgets.QTabWidget()
        layout.addWidget(self.tabwidget)
        self.setLayout(layout)
        self.widgetlist = []
        for data, title, comment in datalist:
            if len(data[0]) == 3:
                widget = FormComboWidget(data, comment=comment, parent=self)
            else:
                widget = FormWidget(data, comment=comment, parent=self)
            index = self.tabwidget.addTab(widget, title)
            self.tabwidget.setTabToolTip(index, comment)
            self.widgetlist.append(widget)

    def setup(self):
        for widget in self.widgetlist:
            widget.setup()

    def get(self):
        return [widget.get() for widget in self.widgetlist]
