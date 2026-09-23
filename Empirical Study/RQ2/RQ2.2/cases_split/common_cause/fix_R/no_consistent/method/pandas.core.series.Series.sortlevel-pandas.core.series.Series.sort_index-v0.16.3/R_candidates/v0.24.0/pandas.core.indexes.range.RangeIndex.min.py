    def min(self, axis=None, skipna=True):
        """The minimum value of the RangeIndex"""
        nv.validate_minmax_axis(axis)
        return self._minmax('min')
