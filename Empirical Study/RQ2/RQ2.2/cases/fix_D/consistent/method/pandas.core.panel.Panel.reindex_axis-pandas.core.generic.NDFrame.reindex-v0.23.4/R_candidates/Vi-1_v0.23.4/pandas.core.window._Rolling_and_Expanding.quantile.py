    def quantile(self, quantile, interpolation='linear', **kwargs):
        window = self._get_window()
        index, indexi = self._get_index()

        def f(arg, *args, **kwargs):
            minp = _use_window(self.min_periods, window)
            if quantile == 1.0:
                return _window.roll_max(arg, window, minp, indexi,
                                        self.closed)
            elif quantile == 0.0:
                return _window.roll_min(arg, window, minp, indexi,
                                        self.closed)
            else:
                return _window.roll_quantile(arg, window, minp, indexi,
                                             self.closed, quantile,
                                             interpolation)

        return self._apply(f, 'quantile', quantile=quantile,
                           **kwargs)
