    @deprecate_kwarg('take_last', 'keep',
                     mapping={True: 'last', False: 'first'})
    @Appender(Series.nlargest.__doc__)
    def nlargest(self, n=5, keep='first'):
        # ToDo: When we remove deprecate_kwargs, we can remote these methods
        # and include nlargest and nsmallest to _series_apply_whitelist
        return self.apply(lambda x: x.nlargest(n=n, keep=keep))
