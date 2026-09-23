    def convert_xunits(self, x):
        """
        Convert *x* using the unit type of the xaxis.

        If the artist is not in contained in an Axes or if the xaxis does not
        have units, *x* itself is returned.
        """
        ax = getattr(self, 'axes', None)
        if ax is None or ax.xaxis is None:
            return x
        return ax.xaxis.convert_units(x)
