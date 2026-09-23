    def _wrap_result(self, result):
        """
        Potentially wrap any results.
        """
        # GH 47705
        obj = self.obj
        if (
            isinstance(result, ABCDataFrame)
            and result.empty
            and not isinstance(result.index, PeriodIndex)
        ):
            result = result.set_index(
                _asfreq_compat(obj.index[:0], freq=self.freq), append=True
            )

        if isinstance(result, ABCSeries) and self._selection is not None:
            result.name = self._selection

        if isinstance(result, ABCSeries) and result.empty:
            # When index is all NaT, result is empty but index is not
            result.index = _asfreq_compat(obj.index[:0], freq=self.freq)
            result.name = getattr(obj, "name", None)

        return result
