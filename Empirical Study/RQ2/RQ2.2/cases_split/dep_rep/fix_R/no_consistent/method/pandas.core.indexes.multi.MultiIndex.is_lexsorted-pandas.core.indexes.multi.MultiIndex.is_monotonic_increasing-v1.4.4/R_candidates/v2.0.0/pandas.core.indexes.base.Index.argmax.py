    @Appender(IndexOpsMixin.argmax.__doc__)
    def argmax(self, axis=None, skipna: bool = True, *args, **kwargs) -> int:
        nv.validate_argmax(args, kwargs)
        nv.validate_minmax_axis(axis)

        if not self._is_multi and self.hasnans:
            # Take advantage of cache
            mask = self._isnan
            if not skipna or mask.all():
                return -1
        return super().argmax(skipna=skipna)
