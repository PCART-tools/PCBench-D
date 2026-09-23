    def _adjust_bin_edges(
        self, binner: DatetimeIndex, ax_values: npt.NDArray[np.int64]
    ) -> tuple[DatetimeIndex, npt.NDArray[np.int64]]:
        # Some hacks for > daily data, see #1471, #1458, #1483

        if self.freq != "D" and is_superperiod(self.freq, "D"):
            if self.closed == "right":
                # GH 21459, GH 9119: Adjust the bins relative to the wall time
                edges_dti = binner.tz_localize(None)
                edges_dti = (
                    edges_dti
                    + Timedelta(days=1, unit=edges_dti.unit).as_unit(edges_dti.unit)
                    - Timedelta(1, unit=edges_dti.unit).as_unit(edges_dti.unit)
                )
                bin_edges = edges_dti.tz_localize(binner.tz).asi8
            else:
                bin_edges = binner.asi8

            # intraday values on last day
            if bin_edges[-2] > ax_values.max():
                bin_edges = bin_edges[:-1]
                binner = binner[:-1]
        else:
            bin_edges = binner.asi8
        return binner, bin_edges
