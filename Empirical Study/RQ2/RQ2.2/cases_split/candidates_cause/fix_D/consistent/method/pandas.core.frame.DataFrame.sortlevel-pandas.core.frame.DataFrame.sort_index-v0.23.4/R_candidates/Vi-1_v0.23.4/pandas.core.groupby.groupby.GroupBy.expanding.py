    @Substitution(name='groupby')
    @Appender(_doc_template)
    def expanding(self, *args, **kwargs):
        """
        Return an expanding grouper, providing expanding
        functionality per group

        """
        from pandas.core.window import ExpandingGroupby
        return ExpandingGroupby(self, *args, **kwargs)
