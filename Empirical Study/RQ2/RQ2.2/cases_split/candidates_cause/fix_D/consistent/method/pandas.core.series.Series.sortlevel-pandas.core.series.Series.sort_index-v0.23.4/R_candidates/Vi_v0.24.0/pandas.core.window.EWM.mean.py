    @Substitution(name='ewm')
    @Appender(_doc_template)
    def mean(self, *args, **kwargs):
        """
        Exponential weighted moving average.

        Parameters
        ----------
        *args, **kwargs
            Arguments and keyword arguments to be passed into func.
        """
        nv.validate_window_func('mean', args, kwargs)
        return self._apply('ewma', **kwargs)
