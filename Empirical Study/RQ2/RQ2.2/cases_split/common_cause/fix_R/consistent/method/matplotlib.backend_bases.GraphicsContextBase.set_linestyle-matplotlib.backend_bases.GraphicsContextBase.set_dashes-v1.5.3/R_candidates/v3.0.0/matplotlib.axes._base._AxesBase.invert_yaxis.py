    def invert_yaxis(self):
        """Invert the y-axis."""
        self.set_ylim(self.get_ylim()[::-1], auto=None)
