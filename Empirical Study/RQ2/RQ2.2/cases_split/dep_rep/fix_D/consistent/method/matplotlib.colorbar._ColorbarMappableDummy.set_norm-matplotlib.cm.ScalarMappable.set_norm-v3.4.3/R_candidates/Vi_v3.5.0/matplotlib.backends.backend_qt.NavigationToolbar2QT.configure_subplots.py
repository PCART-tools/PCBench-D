    def configure_subplots(self):
        image = str(cbook._get_data_path('images/matplotlib.png'))
        self._subplot_dialog = SubplotToolQt(
            self.canvas.figure, self.canvas.parent())
        self._subplot_dialog.setWindowIcon(QtGui.QIcon(image))
        self._subplot_dialog.show()
