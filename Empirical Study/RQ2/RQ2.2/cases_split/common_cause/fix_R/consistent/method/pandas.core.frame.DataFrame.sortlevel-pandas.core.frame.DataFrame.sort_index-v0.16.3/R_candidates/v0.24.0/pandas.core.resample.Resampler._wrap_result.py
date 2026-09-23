    def _wrap_result(self, result):
        """
        Potentially wrap any results.
        """
        if isinstance(result, ABCSeries) and self._selection is not None:
            result.name = self._selection

        if isinstance(result, ABCSeries) and result.empty:
            obj = self.obj
            if isinstance(obj.index, PeriodIndex):
                result.index = obj.index.asfreq(self.freq)
            else:
                result.index = obj.index._shallow_copy(freq=self.freq)
            result.name = getattr(obj, 'name', None)

        return result
