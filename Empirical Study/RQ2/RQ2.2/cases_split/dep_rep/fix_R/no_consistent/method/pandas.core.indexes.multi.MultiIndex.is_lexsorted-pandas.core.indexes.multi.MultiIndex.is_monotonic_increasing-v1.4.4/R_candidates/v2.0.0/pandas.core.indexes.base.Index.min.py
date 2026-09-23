    @doc(IndexOpsMixin.min)
    def min(self, axis=None, skipna: bool = True, *args, **kwargs):
        nv.validate_min(args, kwargs)
        nv.validate_minmax_axis(axis)

        if not len(self):
            return self._na_value

        if len(self) and self.is_monotonic_increasing:
            # quick check
            first = self[0]
            if not isna(first):
                return first

        if not self._is_multi and self.hasnans:
            # Take advantage of cache
            mask = self._isnan
            if not skipna or mask.all():
                return self._na_value

        if not self._is_multi and not isinstance(self._values, np.ndarray):
            return self._values._reduce(name="min", skipna=skipna)

        return super().min(skipna=skipna)
