    def _get_binner_for_time(self):
        return self.groupby._get_time_delta_bins(self.ax)
