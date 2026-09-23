    def quantile(self, quantile, **kwargs):
        window = self._get_window()
        index, indexi = self._get_index()

        def f(arg, *args, **kwargs):
            minp = _use_window(self.min_periods, window)
            return _window.roll_quantile(arg, window, minp, indexi,
                                         quantile)

        return self._apply(f, 'quantile', quantile=quantile,
                           **kwargs)
