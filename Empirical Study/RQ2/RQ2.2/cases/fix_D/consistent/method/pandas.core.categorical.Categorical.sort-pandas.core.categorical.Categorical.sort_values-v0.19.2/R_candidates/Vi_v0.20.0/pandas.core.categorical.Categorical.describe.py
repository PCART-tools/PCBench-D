    def describe(self):
        """ Describes this Categorical

        Returns
        -------
        description: `DataFrame`
            A dataframe with frequency and counts by category.
        """
        counts = self.value_counts(dropna=False)
        freqs = counts / float(counts.sum())

        from pandas.core.reshape.concat import concat
        result = concat([counts, freqs], axis=1)
        result.columns = ['counts', 'freqs']
        result.index.name = 'categories'

        return result
