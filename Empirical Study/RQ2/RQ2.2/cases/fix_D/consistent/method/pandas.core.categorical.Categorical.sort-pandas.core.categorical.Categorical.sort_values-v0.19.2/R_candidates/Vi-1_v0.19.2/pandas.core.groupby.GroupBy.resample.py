    @Substitution(name='groupby')
    @Appender(_doc_template)
    def resample(self, rule, *args, **kwargs):
        """
        Provide resampling when using a TimeGrouper
        Return a new grouper with our resampler appended
        """
        from pandas.tseries.resample import get_resampler_for_grouping
        return get_resampler_for_grouping(self, rule, *args, **kwargs)
