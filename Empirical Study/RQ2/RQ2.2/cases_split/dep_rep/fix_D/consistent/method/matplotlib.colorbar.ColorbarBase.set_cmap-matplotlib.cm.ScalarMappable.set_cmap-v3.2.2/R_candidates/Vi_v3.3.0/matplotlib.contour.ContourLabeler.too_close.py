    def too_close(self, x, y, lw):
        """Return *True* if a label is already near this location."""
        thresh = (1.2 * lw) ** 2
        return any((x - loc[0]) ** 2 + (y - loc[1]) ** 2 < thresh
                   for loc in self.labelXYs)
