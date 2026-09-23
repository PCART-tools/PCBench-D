    def describe(self):
        """
        Returns a dataframe with frequency and counts by level.
        """
        # Hack?
        from pandas.core.frame import DataFrame
        grouped = DataFrame(self.labels).groupby(0)
        counts = grouped.count().values.squeeze()
        freqs = counts / float(counts.sum())
        return DataFrame.from_dict({
            'counts': counts,
            'freqs': freqs,
            'levels': self.levels
        }).set_index('levels')
