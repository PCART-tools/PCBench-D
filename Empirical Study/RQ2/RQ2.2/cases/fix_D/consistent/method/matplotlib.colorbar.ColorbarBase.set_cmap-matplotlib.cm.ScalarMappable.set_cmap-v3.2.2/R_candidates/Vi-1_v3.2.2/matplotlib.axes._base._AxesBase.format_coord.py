    def format_coord(self, x, y):
        """Return a format string formatting the *x*, *y* coordinates."""
        if x is None:
            xs = '???'
        else:
            xs = self.format_xdata(x)
        if y is None:
            ys = '???'
        else:
            ys = self.format_ydata(y)
        return 'x=%s y=%s' % (xs, ys)
