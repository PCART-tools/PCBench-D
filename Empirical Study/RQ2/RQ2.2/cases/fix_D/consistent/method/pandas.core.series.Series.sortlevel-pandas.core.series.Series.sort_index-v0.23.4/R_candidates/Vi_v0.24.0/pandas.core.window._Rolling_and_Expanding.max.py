    def max(self, *args, **kwargs):
        nv.validate_window_func('max', args, kwargs)
        return self._apply('roll_max', 'max', **kwargs)
