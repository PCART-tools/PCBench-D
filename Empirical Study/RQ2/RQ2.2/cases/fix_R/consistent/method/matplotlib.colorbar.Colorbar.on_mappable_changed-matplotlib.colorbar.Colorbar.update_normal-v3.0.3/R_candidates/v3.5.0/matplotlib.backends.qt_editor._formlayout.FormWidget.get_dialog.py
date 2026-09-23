    def get_dialog(self):
        """Return FormDialog instance"""
        dialog = self.parent()
        while not isinstance(dialog, QtWidgets.QDialog):
            dialog = dialog.parent()
        return dialog
