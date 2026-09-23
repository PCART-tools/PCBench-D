    def cov(self, other=None, pairwise=None, ddof=1, **kwargs):
        if other is None:
            other = self._selected_obj
            # only default unset
            pairwise = True if pairwise is None else pairwise
        other = self._shallow_copy(other)
        window = self._get_window(other)

        def _get_cov(X, Y):
            # GH #12373 : rolling functions error on float32 data
            # to avoid potential overflow, cast the data to float64
            X = X.astype('float64')
            Y = Y.astype('float64')
            mean = lambda x: x.rolling(window, self.min_periods,
                                       center=self.center).mean(**kwargs)
            count = (X + Y).rolling(window=window,
                                    center=self.center).count(**kwargs)
            bias_adj = count / (count - ddof)
            return (mean(X * Y) - mean(X) * mean(Y)) * bias_adj

        return _flex_binary_moment(self._selected_obj, other._selected_obj,
                                   _get_cov, pairwise=bool(pairwise))
