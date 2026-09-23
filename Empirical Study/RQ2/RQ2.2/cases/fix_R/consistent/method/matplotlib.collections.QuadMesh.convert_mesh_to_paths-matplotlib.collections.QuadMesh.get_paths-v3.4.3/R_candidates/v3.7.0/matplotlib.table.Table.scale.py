    def scale(self, xscale, yscale):
        """Scale column widths by *xscale* and row heights by *yscale*."""
        for c in self._cells.values():
            c.set_width(c.get_width() * xscale)
            c.set_height(c.get_height() * yscale)
