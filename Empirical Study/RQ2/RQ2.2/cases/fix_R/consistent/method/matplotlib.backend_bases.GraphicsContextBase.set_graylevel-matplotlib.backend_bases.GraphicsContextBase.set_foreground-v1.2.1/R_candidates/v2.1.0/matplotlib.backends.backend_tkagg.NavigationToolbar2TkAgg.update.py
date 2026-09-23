    def update(self):
        _focus = windowing.FocusManager()
        self._axes = self.canvas.figure.axes
        NavigationToolbar2.update(self)
