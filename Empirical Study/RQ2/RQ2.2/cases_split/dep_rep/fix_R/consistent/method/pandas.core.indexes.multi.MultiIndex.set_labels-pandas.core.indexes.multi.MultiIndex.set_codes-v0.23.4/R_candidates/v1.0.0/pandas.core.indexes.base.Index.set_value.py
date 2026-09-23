    def set_value(self, arr, key, value):
        """
        Fast lookup of value from 1-dimensional ndarray.

        .. deprecated:: 1.0

        Notes
        -----
        Only use this if you know what you're doing.
        """
        warnings.warn(
            (
                "The 'set_value' method is deprecated, and "
                "will be removed in a future version."
            ),
            FutureWarning,
            stacklevel=2,
        )
        self._engine.set_value(
            com.values_from_object(arr), com.values_from_object(key), value
        )
