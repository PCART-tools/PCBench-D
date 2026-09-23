    @cache_readonly
    def _values(self) -> np.ndarray:
        # We override here, since our parent uses _data, which we don't use.
        values = []

        for i in range(self.nlevels):
            vals = self._get_level_values(i)
            if is_categorical_dtype(vals.dtype):
                vals = cast("CategoricalIndex", vals)
                vals = vals._data._internal_get_values()
            if isinstance(vals.dtype, ExtensionDtype) or isinstance(
                vals, (ABCDatetimeIndex, ABCTimedeltaIndex)
            ):
                vals = vals.astype(object)
            # error: Incompatible types in assignment (expression has type "ndarray",
            # variable has type "Index")
            vals = np.array(vals, copy=False)  # type: ignore[assignment]
            values.append(vals)

        arr = lib.fast_zip(values)
        return arr
