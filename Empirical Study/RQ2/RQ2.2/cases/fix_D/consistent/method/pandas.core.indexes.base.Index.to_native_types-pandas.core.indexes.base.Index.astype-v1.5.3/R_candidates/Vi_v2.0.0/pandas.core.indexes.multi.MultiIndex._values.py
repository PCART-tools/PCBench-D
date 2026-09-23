    @cache_readonly
    def _values(self) -> np.ndarray:
        # We override here, since our parent uses _data, which we don't use.
        values = []

        for i in range(self.nlevels):
            index = self.levels[i]
            codes = self.codes[i]

            vals = index
            if is_categorical_dtype(vals.dtype):
                vals = cast("CategoricalIndex", vals)
                vals = vals._data._internal_get_values()

            if isinstance(vals.dtype, ExtensionDtype) or isinstance(
                vals, (ABCDatetimeIndex, ABCTimedeltaIndex)
            ):
                vals = vals.astype(object)

            vals = np.array(vals, copy=False)
            vals = algos.take_nd(vals, codes, fill_value=index._na_value)
            values.append(vals)

        arr = lib.fast_zip(values)
        return arr
