    def describe(self):
        """ Describes this Categorical

        Returns
        -------
        description: `DataFrame`
            A dataframe with frequency and counts by category.
        """
        # Hack?
        from pandas.core.frame import DataFrame
        counts = DataFrame({
            'codes' : self._codes,
            'values' : self._codes }
                           ).groupby('codes').count()

        freqs = counts / float(counts.sum())

        from pandas.tools.merge import concat
        result = concat([counts,freqs],axis=1)
        result.columns = ['counts','freqs']

        # fill in the real categories
        check = result.index == -1
        if check.any():
            # Sort -1 (=NaN) to the last position
            index = np.arange(0, len(self.categories)+1, dtype='int64')
            index[-1] = -1
            result = result.reindex(index)
            # build new index
            categories = np.arange(0,len(self.categories)+1 ,dtype=object)
            categories[:-1] = self.categories
            categories[-1] = np.nan
            result.index = categories.take(com._ensure_platform_int(result.index))
        else:
            result.index = self.categories.take(com._ensure_platform_int(result.index))
            result = result.reindex(self.categories)
        result.index.name = 'categories'

        return result
