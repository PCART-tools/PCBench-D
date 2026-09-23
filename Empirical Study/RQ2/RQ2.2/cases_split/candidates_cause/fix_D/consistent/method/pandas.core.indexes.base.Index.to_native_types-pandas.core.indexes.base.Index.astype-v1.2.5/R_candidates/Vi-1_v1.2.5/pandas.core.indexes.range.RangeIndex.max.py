    def max(self, axis=None, skipna=True, *args, **kwargs) -> int:
        """The maximum value of the RangeIndex"""
        nv.validate_minmax_axis(axis)
        nv.validate_max(args, kwargs)
        return self._minmax("max")
