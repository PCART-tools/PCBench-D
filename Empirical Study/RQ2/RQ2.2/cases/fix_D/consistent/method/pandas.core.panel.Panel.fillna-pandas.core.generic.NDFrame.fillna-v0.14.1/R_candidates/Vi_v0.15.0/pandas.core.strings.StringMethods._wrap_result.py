    def _wrap_result(self, result):
        if not hasattr(result, 'ndim'):
            return result
        elif result.ndim == 1:
            name = getattr(result, 'name', None)
            return Series(result, index=self.series.index,
                          name=name or self.series.name)
        else:
            assert result.ndim < 3
            return DataFrame(result, index=self.series.index)
