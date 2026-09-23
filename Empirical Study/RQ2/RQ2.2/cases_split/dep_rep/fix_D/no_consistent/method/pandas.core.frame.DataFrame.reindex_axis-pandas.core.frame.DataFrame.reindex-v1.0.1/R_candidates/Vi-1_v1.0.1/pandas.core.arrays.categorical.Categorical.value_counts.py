    def value_counts(self, dropna=True):
        """
        Return a Series containing counts of each category.

        Every category will have an entry, even those with a count of 0.

        Parameters
        ----------
        dropna : bool, default True
            Don't include counts of NaN.

        Returns
        -------
        counts : Series

        See Also
        --------
        Series.value_counts
        """
        from pandas import Series, CategoricalIndex

        code, cat = self._codes, self.categories
        ncat, mask = len(cat), 0 <= code
        ix, clean = np.arange(ncat), mask.all()

        if dropna or clean:
            obs = code if clean else code[mask]
            count = np.bincount(obs, minlength=ncat or 0)
        else:
            count = np.bincount(np.where(mask, code, ncat))
            ix = np.append(ix, -1)

        ix = self._constructor(ix, dtype=self.dtype, fastpath=True)

        return Series(count, index=CategoricalIndex(ix), dtype="int64")
