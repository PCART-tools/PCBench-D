    def configure_subplots(self):
        image = str(cbook._get_data_path('images/matplotlib.png'))
        dia = SubplotToolQt(self.canvas.figure, self.canvas.parent())
        dia.setWindowIcon(QtGui.QIcon(image))
        dia.exec_()
