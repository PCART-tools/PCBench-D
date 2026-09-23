    def get_extent(self):
        """Return the image extent as tuple (left, right, bottom, top)."""
        numrows, numcols = self.get_size()
        return (-0.5 + self.ox, numcols-0.5 + self.ox,
                -0.5 + self.oy, numrows-0.5 + self.oy)
