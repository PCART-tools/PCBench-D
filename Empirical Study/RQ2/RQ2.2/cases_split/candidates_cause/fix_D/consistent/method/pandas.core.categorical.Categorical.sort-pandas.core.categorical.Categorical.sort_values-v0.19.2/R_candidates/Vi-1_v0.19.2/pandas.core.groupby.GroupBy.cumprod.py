    @Substitution(name='groupby')
    @Appender(_doc_template)
    def cumprod(self, axis=0, *args, **kwargs):
        """Cumulative product for each group"""
        nv.validate_groupby_func('cumprod', args, kwargs)
        if axis != 0:
            return self.apply(lambda x: x.cumprod(axis=axis))

        return self._cython_transform('cumprod')
