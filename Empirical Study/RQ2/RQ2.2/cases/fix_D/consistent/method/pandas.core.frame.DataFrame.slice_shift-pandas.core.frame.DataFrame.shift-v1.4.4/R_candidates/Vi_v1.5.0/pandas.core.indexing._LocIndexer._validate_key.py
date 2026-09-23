    @doc(_LocationIndexer._validate_key)
    def _validate_key(self, key, axis: int):
        # valid for a collection of labels (we check their presence later)
        # slice of labels (where start-end in labels)
        # slice of integers (only if in the labels)
        # boolean not in slice and with boolean index
        if isinstance(key, bool) and not (
            is_bool_dtype(self.obj._get_axis(axis))
            or self.obj._get_axis(axis).dtype.name == "boolean"
        ):
            raise KeyError(
                f"{key}: boolean label can not be used without a boolean index"
            )

        if isinstance(key, slice) and (
            isinstance(key.start, bool) or isinstance(key.stop, bool)
        ):
            raise TypeError(f"{key}: boolean values can not be used in a slice")
