    @Substitution(name='ewm')
    @Appender(_doc_template)
    @Appender(_pairwise_template)
    def corr(self, other=None, pairwise=None, **kwargs):
        """exponential weighted sample correlation"""
        if other is None:
            other = self._selected_obj
            # only default unset
            pairwise = True if pairwise is None else pairwise
        other = self._shallow_copy(other)

        def _get_corr(X, Y):
            X = self._shallow_copy(X)
            Y = self._shallow_copy(Y)

            def _cov(x, y):
                return _window.ewmcov(x, y, self.com, int(self.adjust),
                                      int(self.ignore_na),
                                      int(self.min_periods),
                                      1)

            x_values = X._prep_values()
            y_values = Y._prep_values()
            with np.errstate(all='ignore'):
                cov = _cov(x_values, y_values)
                x_var = _cov(x_values, x_values)
                y_var = _cov(y_values, y_values)
                corr = cov / _zsqrt(x_var * y_var)
            return X._wrap_result(corr)

        return _flex_binary_moment(self._selected_obj, other._selected_obj,
                                   _get_corr, pairwise=bool(pairwise))
