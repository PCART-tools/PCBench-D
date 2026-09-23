    def _should_validate_iterable(self, axis=None):
        """ return a boolean whether this axes needs validation for a passed
        iterable
        """
        if axis is None:
            axis = self.axis or 0
        ax = self.obj._get_axis(axis)
        if isinstance(ax, MultiIndex):
            return False
        elif ax.is_floating():
            return False

        return True
