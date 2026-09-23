    def _wrap_result(self, result):
        assert result.ndim < 3
        if result.ndim == 1:
            return Series(result, index=self.series.index,
                          name=self.series.name)
        else:
            return DataFrame(result, index=self.series.index)
