    def __init__(self, window, *args, **kwargs):
        StatusbarBase.__init__(self, *args, **kwargs)
        QtWidgets.QLabel.__init__(self)
        window.statusBar().addWidget(self)
