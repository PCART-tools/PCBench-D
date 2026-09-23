    def min(self, how=None, *args, **kwargs):
        nv.validate_window_func('min', args, kwargs)
        if self.freq is not None and how is None:
            how = 'min'
        return self._apply('roll_min', 'min', how=how, **kwargs)
