    def format_coord(self, x, y):
        """Return a format string formatting the *x*, *y* coordinates."""
        twins = self._twinned_axes.get_siblings(self)
        if len(twins) == 1:
            return "(x, y) = ({}, {})".format(
                "???" if x is None else self.format_xdata(x),
                "???" if y is None else self.format_ydata(y))
        screen_xy = self.transData.transform((x, y))
        xy_strs = []
        # Retrieve twins in the order of self.figure.axes to sort tied zorders (which is
        # the common case) by the order in which they are added to the figure.
        for ax in sorted(twins, key=attrgetter("zorder")):
            data_x, data_y = ax.transData.inverted().transform(screen_xy)
            xy_strs.append(
                "({}, {})".format(ax.format_xdata(data_x), ax.format_ydata(data_y)))
        return "(x, y) = {}".format(" | ".join(xy_strs))
