    def update(self):
        self._axes = self.canvas.figure.axes
        with _restore_foreground_window_at_end():
            NavigationToolbar2.update(self)
