    @Substitution(name='groupby')
    @Appender(_doc_template)
    def rolling(self, *args, **kwargs):
        """
        Return a rolling grouper, providing rolling
        functionality per group

        """
        from pandas.core.window import RollingGroupby
        return RollingGroupby(self, *args, **kwargs)
