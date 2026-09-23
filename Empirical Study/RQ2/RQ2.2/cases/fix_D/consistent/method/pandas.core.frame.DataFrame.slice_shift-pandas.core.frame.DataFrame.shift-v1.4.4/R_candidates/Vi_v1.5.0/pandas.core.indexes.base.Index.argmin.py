    @Appender(IndexOpsMixin.argmin.__doc__)
    def argmin(self, axis=None, skipna=True, *args, **kwargs) -> int:
        nv.validate_argmin(args, kwargs)
        nv.validate_minmax_axis(axis)

        if not self._is_multi and self.hasnans:
            # Take advantage of cache
            mask = self._isnan
            if not skipna or mask.all():
                return -1
        return super().argmin(skipna=skipna)
