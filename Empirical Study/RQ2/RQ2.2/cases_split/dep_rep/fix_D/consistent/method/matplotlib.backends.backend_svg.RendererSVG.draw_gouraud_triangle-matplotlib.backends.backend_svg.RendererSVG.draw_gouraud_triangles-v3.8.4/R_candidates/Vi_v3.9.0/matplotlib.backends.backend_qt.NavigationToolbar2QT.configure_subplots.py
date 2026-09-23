    def configure_subplots(self):
        if self._subplot_dialog is None:
            self._subplot_dialog = SubplotToolQt(
                self.canvas.figure, self.canvas.parent())
            self.canvas.mpl_connect(
                "close_event", lambda e: self._subplot_dialog.reject())
        self._subplot_dialog.update_from_current_subplotpars()
        self._subplot_dialog.setModal(True)
        self._subplot_dialog.show()
        return self._subplot_dialog
