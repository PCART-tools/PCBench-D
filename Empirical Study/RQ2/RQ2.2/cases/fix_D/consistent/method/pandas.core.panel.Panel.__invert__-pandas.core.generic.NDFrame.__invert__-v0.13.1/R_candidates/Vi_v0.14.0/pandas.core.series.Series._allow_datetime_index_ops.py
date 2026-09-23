    @property
    def _allow_datetime_index_ops(self):
        # disabling to invalidate datetime index ops (GH7206)
        # return self.index.is_all_dates and isinstance(self.index, DatetimeIndex)
        return False
