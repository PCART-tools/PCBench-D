    def closeEvent(self, event):
        self.closing.emit()
        super().closeEvent(event)
