    def _convert_tolerance(self, tolerance, target):
        tolerance = np.asarray(to_timedelta(tolerance).to_numpy())

        if target.size != tolerance.size and tolerance.size > 1:
            raise ValueError("list-like tolerance size must match " "target index size")
        return tolerance
