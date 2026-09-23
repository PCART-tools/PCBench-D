    def where(
        self,
        other,
        cond,
        align=True,
        errors="raise",
        try_cast: bool = False,
        axis: int = 0,
    ) -> List["Block"]:
        if isinstance(other, ABCDataFrame):
            # ExtensionArrays are 1-D, so if we get here then
            # `other` should be a DataFrame with a single column.
            assert other.shape[1] == 1
            other = other.iloc[:, 0]

        other = extract_array(other, extract_numpy=True)

        if isinstance(cond, ABCDataFrame):
            assert cond.shape[1] == 1
            cond = cond.iloc[:, 0]

        cond = extract_array(cond, extract_numpy=True)

        if lib.is_scalar(other) and isna(other):
            # The default `other` for Series / Frame is np.nan
            # we want to replace that with the correct NA value
            # for the type
            other = self.dtype.na_value

        if is_sparse(self.values):
            # TODO(SparseArray.__setitem__): remove this if condition
            # We need to re-infer the type of the data after doing the
            # where, for cases where the subtypes don't match
            dtype = None
        else:
            dtype = self.dtype

        result = self.values.copy()
        icond = ~cond
        if lib.is_scalar(other):
            set_other = other
        else:
            set_other = other[icond]
        try:
            result[icond] = set_other
        except (NotImplementedError, TypeError):
            # NotImplementedError for class not implementing `__setitem__`
            # TypeError for SparseArray, which implements just to raise
            # a TypeError
            result = self._holder._from_sequence(
                np.where(cond, self.values, other), dtype=dtype
            )

        return [self.make_block_same_class(result, placement=self.mgr_locs)]
