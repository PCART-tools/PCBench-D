    def mean(self, *args, **kwargs):
        nv.validate_window_func('mean', args, kwargs)
        return self._apply('roll_mean', 'mean', **kwargs)
