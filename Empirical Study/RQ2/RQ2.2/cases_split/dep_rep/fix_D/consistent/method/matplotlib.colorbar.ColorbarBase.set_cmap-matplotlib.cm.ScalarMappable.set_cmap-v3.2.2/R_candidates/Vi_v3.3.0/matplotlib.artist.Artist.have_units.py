    def have_units(self):
        """Return *True* if units are set on any axis."""
        ax = self.axes
        return ax and any(axis.have_units() for axis in ax._get_axis_list())
