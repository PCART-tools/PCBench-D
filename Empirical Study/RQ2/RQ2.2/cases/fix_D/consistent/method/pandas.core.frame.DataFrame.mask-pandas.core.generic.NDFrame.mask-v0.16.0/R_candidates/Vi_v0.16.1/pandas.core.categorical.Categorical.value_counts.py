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
        import pandas.hashtable as htable
        from pandas.core.series import Series

        cat = self.dropna() if dropna else self
        keys, counts = htable.value_count_int64(com._ensure_int64(cat._codes))
        result = Series(counts, index=keys)

        ix = np.arange(len(cat.categories), dtype='int64')
        if not dropna and -1 in keys:
            ix = np.append(ix, -1)
        result = result.reindex(ix, fill_value=0)
        result.index = (np.append(cat.categories, np.nan)
            if not dropna and -1 in keys
            else cat.categories)

        return result
