    @Appender(IndexOpsMixin.argmax.__doc__)
    def argmax(self, axis=None, skipna: bool = True, *args, **kwargs) -> int:
        nv.validate_argmax(args, kwargs)
        nv.validate_minmax_axis(axis)

        if not self._is_multi and self.hasnans:
            # Take advantage of cache
            mask = self._isnan
            if not skipna or mask.all():
                warnings.warn(
                    f"The behavior of {type(self).__name__}.argmax/argmin "
                    "with skipna=False and NAs, or with all-NAs is deprecated. "
                    "In a future version this will raise ValueError.",
                    FutureWarning,
                    stacklevel=find_stack_level(),
                )
                return -1
        return super().argmax(skipna=skipna)
