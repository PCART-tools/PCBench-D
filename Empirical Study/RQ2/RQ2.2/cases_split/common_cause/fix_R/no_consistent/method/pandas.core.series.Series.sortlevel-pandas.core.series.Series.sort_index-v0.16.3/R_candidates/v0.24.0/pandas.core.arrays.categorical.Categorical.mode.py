    def mode(self, dropna=True):
        """
        Returns the mode(s) of the Categorical.

        Always returns `Categorical` even if only one value.

        Parameters
        ----------
        dropna : boolean, default True
            Don't consider counts of NaN/NaT.

            .. versionadded:: 0.24.0

        Returns
        -------
        modes : `Categorical` (sorted)
        """

        import pandas._libs.hashtable as htable
        codes = self._codes
        if dropna:
            good = self._codes != -1
            codes = self._codes[good]
        codes = sorted(htable.mode_int64(ensure_int64(codes), dropna))
        return self._constructor(values=codes, dtype=self.dtype, fastpath=True)
