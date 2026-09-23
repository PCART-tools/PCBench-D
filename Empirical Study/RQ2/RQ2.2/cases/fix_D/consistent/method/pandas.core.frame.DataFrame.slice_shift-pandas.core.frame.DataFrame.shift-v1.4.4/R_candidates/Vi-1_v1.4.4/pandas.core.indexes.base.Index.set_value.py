    @final
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
            stacklevel=find_stack_level(),
        )
        loc = self._engine.get_loc(key)
        if not can_hold_element(arr, value):
            raise ValueError
        arr[loc] = value
