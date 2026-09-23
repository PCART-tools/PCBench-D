    def _apply_empty_result(self, func, axis, reduce):
        if reduce is None:
            reduce = False
            try:
                reduce = not isinstance(func(_EMPTY_SERIES), Series)
            except Exception:
                pass

        if reduce:
            return Series(NA, index=self._get_agg_axis(axis))
        else:
            return self.copy()
