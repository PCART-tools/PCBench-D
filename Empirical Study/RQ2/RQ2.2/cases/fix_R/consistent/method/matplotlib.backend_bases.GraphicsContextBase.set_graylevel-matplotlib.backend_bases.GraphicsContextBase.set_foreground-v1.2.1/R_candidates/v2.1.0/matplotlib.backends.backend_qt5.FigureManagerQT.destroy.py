    def destroy(self, *args):
        # check for qApp first, as PySide deletes it in its atexit handler
        if QtWidgets.QApplication.instance() is None:
            return
        if self.window._destroying:
            return
        self.window._destroying = True
        self.window.destroyed.connect(self._widgetclosed)
        if self.toolbar:
            self.toolbar.destroy()
        self.window.close()
