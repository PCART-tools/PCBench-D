    def _wrap_result(self, result):
        """ potentially wrap any results """
        if isinstance(result, ABCSeries) and self._selection is not None:
            result.name = self._selection

        if isinstance(result, ABCSeries) and result.empty:
            obj = self.obj
            result.index = obj.index._shallow_copy(freq=to_offset(self.freq))
            result.name = getattr(obj, 'name', None)

        return result
