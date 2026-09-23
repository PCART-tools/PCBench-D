    @Substitution(name='ewm')
    @Appender(_doc_template)
    @Appender(_pairwise_template)
    def cov(self, other=None, pairwise=None, bias=False, **kwargs):
        """exponential weighted sample covariance"""
        if other is None:
            other = self._selected_obj
            # only default unset
            pairwise = True if pairwise is None else pairwise
        other = self._shallow_copy(other)

        def _get_cov(X, Y):
            X = self._shallow_copy(X)
            Y = self._shallow_copy(Y)
            cov = _window.ewmcov(X._prep_values(), Y._prep_values(), self.com,
                                 int(self.adjust), int(self.ignore_na),
                                 int(self.min_periods), int(bias))
            return X._wrap_result(cov)

        return _flex_binary_moment(self._selected_obj, other._selected_obj,
                                   _get_cov, pairwise=bool(pairwise))
