    def _adjust_bin_edges(self, binner, ax_values):
        # Some hacks for > daily data, see #1471, #1458, #1483

        bin_edges = binner.asi8

        if self.freq != 'D' and is_superperiod(self.freq, 'D'):
            day_nanos = delta_to_nanoseconds(timedelta(1))
            if self.closed == 'right':
                bin_edges = bin_edges + day_nanos - 1

            # intraday values on last day
            if bin_edges[-2] > ax_values.max():
                bin_edges = bin_edges[:-1]
                binner = binner[:-1]

        return binner, bin_edges
