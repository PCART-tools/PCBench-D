    def _apply_empty_result(self, func, axis, reduce, *args, **kwds):
        if reduce is None:
            reduce = False
            try:
                reduce = not isinstance(func(_EMPTY_SERIES, *args, **kwds),
                                        Series)
            except Exception:
                pass

        if reduce:
            return Series(np.nan, index=self._get_agg_axis(axis))
        else:
            return self.copy()
