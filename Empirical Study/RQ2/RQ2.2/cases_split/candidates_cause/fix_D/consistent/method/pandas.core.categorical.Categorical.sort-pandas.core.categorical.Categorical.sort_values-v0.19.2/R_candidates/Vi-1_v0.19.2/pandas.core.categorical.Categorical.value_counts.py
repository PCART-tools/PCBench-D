    def value_counts(self, dropna=True):
        """
        Returns a Series containing counts of each category.

        Every category will have an entry, even those with a count of 0.

        Parameters
        ----------
        dropna : boolean, default True
            Don't include counts of NaN, even if NaN is a category.

        Returns
        -------
        counts : Series
        """
        from numpy import bincount
        from pandas.types.missing import isnull
        from pandas.core.series import Series
        from pandas.core.index import CategoricalIndex

        obj = (self.remove_categories([np.nan]) if dropna and
               isnull(self.categories).any() else self)
        code, cat = obj._codes, obj.categories
        ncat, mask = len(cat), 0 <= code
        ix, clean = np.arange(ncat), mask.all()

        if dropna or clean:
            obs = code if clean else code[mask]
            count = bincount(obs, minlength=ncat or None)
        else:
            count = bincount(np.where(mask, code, ncat))
            ix = np.append(ix, -1)

        ix = self._constructor(ix, categories=cat, ordered=obj.ordered,
                               fastpath=True)

        return Series(count, index=CategoricalIndex(ix), dtype='int64')
