    def _get_binner_for_time(self):
        if self.kind == 'timestamp':
            return super(PeriodIndexResampler, self)._get_binner_for_time()
        return self.groupby._get_period_bins(self.ax)
