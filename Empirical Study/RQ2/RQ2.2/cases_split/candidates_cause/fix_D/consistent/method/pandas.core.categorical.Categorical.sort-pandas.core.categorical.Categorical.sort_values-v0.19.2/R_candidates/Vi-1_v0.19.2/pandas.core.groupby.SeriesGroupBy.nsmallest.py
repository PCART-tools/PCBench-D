    @deprecate_kwarg('take_last', 'keep',
                     mapping={True: 'last', False: 'first'})
    @Appender(Series.nsmallest.__doc__)
    def nsmallest(self, n=5, keep='first'):
        return self.apply(lambda x: x.nsmallest(n=n, keep=keep))
