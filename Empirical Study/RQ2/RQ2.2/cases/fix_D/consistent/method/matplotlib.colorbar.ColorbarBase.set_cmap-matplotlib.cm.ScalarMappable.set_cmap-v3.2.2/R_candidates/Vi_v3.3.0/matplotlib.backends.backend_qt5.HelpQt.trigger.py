    def trigger(self, *args):
        QtWidgets.QMessageBox.information(None, "Help", self._get_help_html())
