    def max(self, how=None, *args, **kwargs):
        nv.validate_window_func('max', args, kwargs)
        if self.freq is not None and how is None:
            how = 'max'
        return self._apply('roll_max', 'max', how=how, **kwargs)
