    def _wrap_difference_result(self, other, result):
        # We will override for MultiIndex to handle empty results
        return self._wrap_setop_result(other, result)
