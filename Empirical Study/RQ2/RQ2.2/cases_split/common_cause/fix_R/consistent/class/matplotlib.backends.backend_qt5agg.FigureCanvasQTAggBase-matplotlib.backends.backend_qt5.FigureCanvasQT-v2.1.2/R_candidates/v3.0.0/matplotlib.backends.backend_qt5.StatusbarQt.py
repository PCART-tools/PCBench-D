class StatusbarQt(StatusbarBase, QtWidgets.QLabel):
    def __init__(self, window, *args, **kwargs):
        StatusbarBase.__init__(self, *args, **kwargs)
        QtWidgets.QLabel.__init__(self)
        window.statusBar().addWidget(self)

    def set_message(self, s):
        self.setText(s)
