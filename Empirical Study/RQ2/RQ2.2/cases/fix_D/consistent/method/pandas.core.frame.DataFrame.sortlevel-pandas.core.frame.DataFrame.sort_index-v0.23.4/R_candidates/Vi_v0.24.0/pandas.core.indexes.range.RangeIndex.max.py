    def max(self, axis=None, skipna=True):
        """The maximum value of the RangeIndex"""
        nv.validate_minmax_axis(axis)
        return self._minmax('max')
