    def describe(self):
        """
        Returns a dataframe with frequency and counts by level.
        """
        # Hack?
        from pandas.core.frame import DataFrame
        counts = DataFrame({
            'labels' : self.labels,
            'values' : self.labels }
                           ).groupby('labels').count().squeeze().values
        freqs = counts / float(counts.sum())
        return DataFrame({
            'counts': counts,
            'freqs': freqs,
            'levels': self.levels
            }).set_index('levels')
