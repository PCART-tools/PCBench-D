    def show(self):
        if self.canvas.figure.stale:
            self.canvas.draw_idle()
        if not self._shown:
            self._show()
            self._shown = True
        if mpl.rcParams["figure.raise_window"]:
            self._raise()
