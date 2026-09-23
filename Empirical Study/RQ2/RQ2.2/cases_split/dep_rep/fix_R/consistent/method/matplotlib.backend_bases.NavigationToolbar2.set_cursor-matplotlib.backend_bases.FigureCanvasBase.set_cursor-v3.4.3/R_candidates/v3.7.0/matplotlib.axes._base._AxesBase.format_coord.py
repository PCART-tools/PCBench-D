    def format_coord(self, x, y):
        """Return a format string formatting the *x*, *y* coordinates."""
        return "x={} y={}".format(
            "???" if x is None else self.format_xdata(x),
            "???" if y is None else self.format_ydata(y),
        )
