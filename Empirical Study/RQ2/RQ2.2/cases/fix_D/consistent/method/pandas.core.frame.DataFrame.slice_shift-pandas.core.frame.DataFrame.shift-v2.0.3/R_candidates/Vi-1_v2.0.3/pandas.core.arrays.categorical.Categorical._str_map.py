    def _str_map(
        self, f, na_value=np.nan, dtype=np.dtype("object"), convert: bool = True
    ):
        # Optimization to apply the callable `f` to the categories once
        # and rebuild the result by `take`ing from the result with the codes.
        # Returns the same type as the object-dtype implementation though.
        from pandas.core.arrays import PandasArray

        categories = self.categories
        codes = self.codes
        result = PandasArray(categories.to_numpy())._str_map(f, na_value, dtype)
        return take_nd(result, codes, fill_value=na_value)
