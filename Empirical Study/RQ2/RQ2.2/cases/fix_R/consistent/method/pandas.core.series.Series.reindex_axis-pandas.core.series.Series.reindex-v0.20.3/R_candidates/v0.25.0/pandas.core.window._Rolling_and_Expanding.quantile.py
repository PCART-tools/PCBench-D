    def quantile(self, quantile, interpolation="linear", **kwargs):
        window = self._get_window()
        index_as_array = self._get_index()

        def f(arg, *args, **kwargs):
            minp = _use_window(self.min_periods, window)
            if quantile == 1.0:
                return libwindow.roll_max(
                    arg, window, minp, index_as_array, self.closed
                )
            elif quantile == 0.0:
                return libwindow.roll_min(
                    arg, window, minp, index_as_array, self.closed
                )
            else:
                return libwindow.roll_quantile(
                    arg,
                    window,
                    minp,
                    index_as_array,
                    self.closed,
                    quantile,
                    interpolation,
                )

        return self._apply(f, "quantile", quantile=quantile, **kwargs)
