    @Substitution(name='ewm')
    @Appender(_doc_template)
    def mean(self, *args, **kwargs):
        """exponential weighted moving average"""
        nv.validate_window_func('mean', args, kwargs)
        return self._apply('ewma', **kwargs)
