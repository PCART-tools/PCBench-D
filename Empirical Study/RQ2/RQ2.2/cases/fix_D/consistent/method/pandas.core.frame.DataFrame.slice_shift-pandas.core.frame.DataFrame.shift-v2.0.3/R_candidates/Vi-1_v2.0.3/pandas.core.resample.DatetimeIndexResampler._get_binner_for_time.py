    def _get_binner_for_time(self):
        # this is how we are actually creating the bins
        if self.kind == "period":
            return self._timegrouper._get_time_period_bins(self.ax)
        return self._timegrouper._get_time_bins(self.ax)
