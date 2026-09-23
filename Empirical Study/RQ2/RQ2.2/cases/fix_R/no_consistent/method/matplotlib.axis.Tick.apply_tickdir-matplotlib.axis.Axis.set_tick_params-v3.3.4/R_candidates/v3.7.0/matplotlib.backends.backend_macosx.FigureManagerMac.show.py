    def show(self):
        if not self._shown:
            self._show()
            self._shown = True
        if mpl.rcParams["figure.raise_window"]:
            self._raise()
