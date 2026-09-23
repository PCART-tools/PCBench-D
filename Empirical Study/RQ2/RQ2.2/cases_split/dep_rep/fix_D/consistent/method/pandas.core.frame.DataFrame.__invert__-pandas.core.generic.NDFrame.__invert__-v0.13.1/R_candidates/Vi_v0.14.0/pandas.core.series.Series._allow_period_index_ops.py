    @property
    def _allow_period_index_ops(self):
        # disabling to invalidate period index ops (GH7206)
        # return self.index.is_all_dates and isinstance(self.index, PeriodIndex)
        return False
