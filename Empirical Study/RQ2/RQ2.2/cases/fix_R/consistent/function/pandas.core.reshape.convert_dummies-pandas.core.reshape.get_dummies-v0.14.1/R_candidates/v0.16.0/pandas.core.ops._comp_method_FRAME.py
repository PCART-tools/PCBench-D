def _comp_method_FRAME(func, name, str_rep, masker=False):
    @Appender('Wrapper for comparison method %s' % name)
    def f(self, other):
        if isinstance(other, pd.DataFrame):    # Another DataFrame
            return self._compare_frame(other, func, str_rep)
        elif isinstance(other, pd.Series):
            return self._combine_series_infer(other, func)
        else:

            # straight boolean comparisions we want to allow all columns
            # (regardless of dtype to pass thru) See #4537 for discussion.
            res = self._combine_const(other, func, raise_on_error=False)
            return res.fillna(True).astype(bool)

    f.__name__ = name

    return f
