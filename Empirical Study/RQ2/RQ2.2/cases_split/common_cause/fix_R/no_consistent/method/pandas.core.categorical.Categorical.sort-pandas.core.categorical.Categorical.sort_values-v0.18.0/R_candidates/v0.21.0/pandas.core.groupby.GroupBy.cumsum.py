    @Substitution(name='groupby')
    @Appender(_doc_template)
    def cumsum(self, axis=0, *args, **kwargs):
        """Cumulative sum for each group"""
        nv.validate_groupby_func('cumsum', args, kwargs, ['numeric_only'])
        if axis != 0:
            return self.apply(lambda x: x.cumsum(axis=axis, **kwargs))

        return self._cython_transform('cumsum', **kwargs)
