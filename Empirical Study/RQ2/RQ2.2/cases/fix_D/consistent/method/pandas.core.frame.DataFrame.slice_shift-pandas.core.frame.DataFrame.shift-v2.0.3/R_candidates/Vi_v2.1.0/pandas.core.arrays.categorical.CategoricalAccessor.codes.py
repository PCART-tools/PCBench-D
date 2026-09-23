    @property
    def codes(self) -> Series:
        """
        Return Series of codes as well as the index.

        Examples
        --------
        >>> raw_cate = pd.Categorical(["a", "b", "c", "a"], categories=["a", "b"])
        >>> ser = pd.Series(raw_cate)
        >>> ser.cat.codes
        0   0
        1   1
        2  -1
        3   0
        dtype: int8
        """
        from pandas import Series

        return Series(self._parent.codes, index=self._index)
