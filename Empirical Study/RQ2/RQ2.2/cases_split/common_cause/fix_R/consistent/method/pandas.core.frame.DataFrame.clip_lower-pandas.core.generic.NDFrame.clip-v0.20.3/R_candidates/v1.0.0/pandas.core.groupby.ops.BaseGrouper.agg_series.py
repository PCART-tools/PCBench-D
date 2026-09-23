    def agg_series(self, obj: Series, func):
        # Caller is responsible for checking ngroups != 0
        assert self.ngroups != 0

        if len(obj) == 0:
            # SeriesGrouper would raise if we were to call _aggregate_series_fast
            return self._aggregate_series_pure_python(obj, func)

        elif is_extension_array_dtype(obj.dtype):
            # _aggregate_series_fast would raise TypeError when
            #  calling libreduction.Slider
            # In the datetime64tz case it would incorrectly cast to tz-naive
            # TODO: can we get a performant workaround for EAs backed by ndarray?
            return self._aggregate_series_pure_python(obj, func)

        elif obj.index._has_complex_internals:
            # Pre-empt TypeError in _aggregate_series_fast
            return self._aggregate_series_pure_python(obj, func)

        try:
            return self._aggregate_series_fast(obj, func)
        except ValueError as err:
            if "Function does not reduce" in str(err):
                # raised in libreduction
                pass
            else:
                raise
        return self._aggregate_series_pure_python(obj, func)
