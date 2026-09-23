    def __call__(self, x, pos=None):
        """
        Return the format for tick val `x` based on the width of the
        axis.

        The position `pos` is ignored.
        """
        xmin, xmax = self.axis.get_view_interval()
        d = abs(xmax - xmin)

        return self.pprint_val(x, d)
