    @doc(IndexOpsMixin.max)
    def max(self, axis=None, skipna=True, *args, **kwargs):
        nv.validate_max(args, kwargs)
        nv.validate_minmax_axis(axis)

        if not len(self):
            return self._na_value

        if len(self) and self.is_monotonic_increasing:
            # quick check
            last = self[-1]
            if not isna(last):
                return last

        if not self._is_multi and self.hasnans:
            # Take advantage of cache
            mask = self._isnan
            if not skipna or mask.all():
                return self._na_value

        if not self._is_multi and not isinstance(self._values, np.ndarray):
            # "ExtensionArray" has no attribute "max"
            return self._values.max(skipna=skipna)  # type: ignore[attr-defined]

        return super().max(skipna=skipna)
