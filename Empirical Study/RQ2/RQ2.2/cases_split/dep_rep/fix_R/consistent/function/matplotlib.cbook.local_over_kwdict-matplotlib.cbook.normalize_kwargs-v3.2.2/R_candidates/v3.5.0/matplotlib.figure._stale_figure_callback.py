def _stale_figure_callback(self, val):
    if self.figure:
        self.figure.stale = val
