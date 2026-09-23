    @doc(_LocationIndexer._validate_key)
    def _validate_key(self, key, axis: Axis):
        # valid for a collection of labels (we check their presence later)
        # slice of labels (where start-end in labels)
        # slice of integers (only if in the labels)
        # boolean not in slice and with boolean index
        ax = self.obj._get_axis(axis)
        if isinstance(key, bool) and not (
            is_bool_dtype(ax)
            or ax.dtype.name == "boolean"
            or isinstance(ax, MultiIndex)
            and is_bool_dtype(ax.get_level_values(0))
        ):
            raise KeyError(
                f"{key}: boolean label can not be used without a boolean index"
            )

        if isinstance(key, slice) and (
            isinstance(key.start, bool) or isinstance(key.stop, bool)
        ):
            raise TypeError(f"{key}: boolean values can not be used in a slice")
