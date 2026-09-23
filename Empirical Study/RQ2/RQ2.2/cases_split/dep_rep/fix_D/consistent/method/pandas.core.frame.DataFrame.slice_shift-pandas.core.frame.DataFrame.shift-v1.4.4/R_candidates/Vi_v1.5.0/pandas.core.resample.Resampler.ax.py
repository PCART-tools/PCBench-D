    @property
    def ax(self):
        # we can infer that this is a PeriodIndex/DatetimeIndex/TimedeltaIndex,
        #  but skipping annotating bc the overrides overwhelming
        return self.groupby.ax
