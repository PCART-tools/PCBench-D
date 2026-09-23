    def min(self, axis=None, skipna=True, *args, **kwargs) -> int:
        """The minimum value of the RangeIndex"""
        nv.validate_minmax_axis(axis)
        nv.validate_min(args, kwargs)
        return self._minmax("min")
