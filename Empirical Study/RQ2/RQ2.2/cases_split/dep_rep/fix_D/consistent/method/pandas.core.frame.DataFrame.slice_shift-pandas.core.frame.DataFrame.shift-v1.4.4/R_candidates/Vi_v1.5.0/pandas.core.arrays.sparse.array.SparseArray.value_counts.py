    def value_counts(self, dropna: bool = True) -> Series:
        """
        Returns a Series containing counts of unique values.

        Parameters
        ----------
        dropna : bool, default True
            Don't include counts of NaN, even if NaN is in sp_values.

        Returns
        -------
        counts : Series
        """
        from pandas import (
            Index,
            Series,
        )

        keys, counts = algos.value_counts_arraylike(self.sp_values, dropna=dropna)
        fcounts = self.sp_index.ngaps
        if fcounts > 0 and (not self._null_fill_value or not dropna):
            mask = isna(keys) if self._null_fill_value else keys == self.fill_value
            if mask.any():
                counts[mask] += fcounts
            else:
                # error: Argument 1 to "insert" has incompatible type "Union[
                # ExtensionArray,ndarray[Any, Any]]"; expected "Union[
                # _SupportsArray[dtype[Any]], Sequence[_SupportsArray[dtype
                # [Any]]], Sequence[Sequence[_SupportsArray[dtype[Any]]]],
                # Sequence[Sequence[Sequence[_SupportsArray[dtype[Any]]]]], Sequence
                # [Sequence[Sequence[Sequence[_SupportsArray[dtype[Any]]]]]]]"
                keys = np.insert(keys, 0, self.fill_value)  # type: ignore[arg-type]
                counts = np.insert(counts, 0, fcounts)

        if not isinstance(keys, ABCIndex):
            index = Index(keys)
        else:
            index = keys
        return Series(counts, index=index)
