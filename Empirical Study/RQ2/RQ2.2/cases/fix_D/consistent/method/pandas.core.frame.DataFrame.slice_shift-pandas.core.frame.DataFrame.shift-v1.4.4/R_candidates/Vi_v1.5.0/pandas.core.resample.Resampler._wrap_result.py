    def _wrap_result(self, result):
        """
        Potentially wrap any results.
        """
        if isinstance(result, ABCSeries) and self._selection is not None:
            result.name = self._selection

        if isinstance(result, ABCSeries) and result.empty:
            obj = self.obj
            # When index is all NaT, result is empty but index is not
            result.index = _asfreq_compat(obj.index[:0], freq=self.freq)
            result.name = getattr(obj, "name", None)

        return result
