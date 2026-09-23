    def accept(self):
        self.data = self.formwidget.get()
        QtWidgets.QDialog.accept(self)
