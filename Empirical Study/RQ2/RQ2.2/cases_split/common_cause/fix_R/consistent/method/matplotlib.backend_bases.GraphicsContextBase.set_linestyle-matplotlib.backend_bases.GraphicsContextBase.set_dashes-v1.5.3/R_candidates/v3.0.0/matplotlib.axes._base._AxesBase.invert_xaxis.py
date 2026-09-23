    def invert_xaxis(self):
        """Invert the x-axis."""
        self.set_xlim(self.get_xlim()[::-1], auto=None)
