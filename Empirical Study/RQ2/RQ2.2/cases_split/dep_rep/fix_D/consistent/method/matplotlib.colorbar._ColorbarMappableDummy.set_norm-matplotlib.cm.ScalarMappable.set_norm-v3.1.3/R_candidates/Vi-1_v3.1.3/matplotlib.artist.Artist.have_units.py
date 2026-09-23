    def have_units(self):
        """Return *True* if units are set on the *x* or *y* axes."""
        ax = self.axes
        if ax is None or ax.xaxis is None:
            return False
        return ax.xaxis.have_units() or ax.yaxis.have_units()
