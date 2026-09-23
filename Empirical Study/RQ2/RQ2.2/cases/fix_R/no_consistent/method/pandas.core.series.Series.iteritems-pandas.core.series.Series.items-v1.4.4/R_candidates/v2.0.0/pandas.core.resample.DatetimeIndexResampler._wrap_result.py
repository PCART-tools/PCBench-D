    def _wrap_result(self, result):
        result = super()._wrap_result(result)

        # we may have a different kind that we were asked originally
        # convert if needed
        if self.kind == "period" and not isinstance(result.index, PeriodIndex):
            result.index = result.index.to_period(self.freq)
        return result
