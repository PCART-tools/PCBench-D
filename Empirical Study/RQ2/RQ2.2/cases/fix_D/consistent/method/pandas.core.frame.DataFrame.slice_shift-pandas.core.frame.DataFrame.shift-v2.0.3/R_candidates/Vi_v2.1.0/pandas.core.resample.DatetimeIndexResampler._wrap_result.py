    def _wrap_result(self, result):
        result = super()._wrap_result(result)

        # we may have a different kind that we were asked originally
        # convert if needed
        if self.kind == "period" and not isinstance(result.index, PeriodIndex):
            if isinstance(result.index, MultiIndex):
                # GH 24103 - e.g. groupby resample
                if not isinstance(result.index.levels[-1], PeriodIndex):
                    new_level = result.index.levels[-1].to_period(self.freq)
                    result.index = result.index.set_levels(new_level, level=-1)
            else:
                result.index = result.index.to_period(self.freq)
        return result
