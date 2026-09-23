    @Substitution(klass="DatetimeIndex")
    @Appender(_shared_docs["searchsorted"])
    def searchsorted(self, value, side="left", sorter=None):
        if isinstance(value, (np.ndarray, Index)):
            if not type(self._data)._is_recognized_dtype(value):
                raise TypeError(
                    "searchsorted requires compatible dtype or scalar, "
                    f"not {type(value).__name__}"
                )
            value = type(self._data)(value)
            self._data._check_compatible_with(value)

        elif isinstance(value, self._data._recognized_scalars):
            self._data._check_compatible_with(value)
            value = self._data._scalar_type(value)

        elif not isinstance(value, DatetimeArray):
            raise TypeError(
                "searchsorted requires compatible dtype or scalar, "
                f"not {type(value).__name__}"
            )

        return self._data.searchsorted(value, side=side)
