    def closeEvent(self, event):
        self.closing.emit()
        QtWidgets.QMainWindow.closeEvent(self, event)
