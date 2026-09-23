    def _wrap_result(self, result):
        """ potentially wrap any results """
        if isinstance(result, com.ABCSeries) and self._selection is not None:
            result.name = self._selection

        return result
