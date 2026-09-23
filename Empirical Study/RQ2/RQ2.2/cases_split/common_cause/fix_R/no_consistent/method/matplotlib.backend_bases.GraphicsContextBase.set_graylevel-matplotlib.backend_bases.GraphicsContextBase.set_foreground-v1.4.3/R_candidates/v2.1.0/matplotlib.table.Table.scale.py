    def scale(self, xscale, yscale):
        """ Scale column widths by xscale and row heights by yscale. """
        for c in six.itervalues(self._cells):
            c.set_width(c.get_width() * xscale)
            c.set_height(c.get_height() * yscale)
