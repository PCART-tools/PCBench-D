    @doc(Index.astype)
    def astype(self, dtype: Dtype, copy: bool = True) -> Index:
        from pandas.core.api import NumericIndex

        dtype = pandas_dtype(dtype)

        categories = self.categories
        # the super method always returns Int64Index, UInt64Index and Float64Index
        # but if the categories are a NumericIndex with dtype float32, we want to
        # return an index with the same dtype as self.categories.
        if categories._is_backward_compat_public_numeric_index:
            assert isinstance(categories, NumericIndex)  # mypy complaint fix
            try:
                categories._validate_dtype(dtype)
            except ValueError:
                pass
            else:
                new_values = self._data.astype(dtype, copy=copy)
                # pass copy=False because any copying has been done in the
                #  _data.astype call above
                return categories._constructor(new_values, name=self.name, copy=False)

        return super().astype(dtype, copy=copy)
