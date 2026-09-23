    def _wrap_result(self, result):
        if not hasattr(result, 'ndim'):
            return result
        elif result.ndim == 1:
            return Series(result, index=self.series.index,
                          name=self.series.name)
        else:
            assert result.ndim < 3
            return DataFrame(result, index=self.series.index)
