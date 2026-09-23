    def get_minorticklocs(self):
        """Return this Axis' minor tick locations in data coordinates."""
        # Remove minor ticks duplicating major ticks.
        major_locs = self.major.locator()
        minor_locs = self.minor.locator()
        transform = self._scale.get_transform()
        tr_minor_locs = transform.transform(minor_locs)
        tr_major_locs = transform.transform(major_locs)
        lo, hi = sorted(transform.transform(self.get_view_interval()))
        # Use the transformed view limits as scale.  1e-5 is the default rtol
        # for np.isclose.
        tol = (hi - lo) * 1e-5
        if self.remove_overlapping_locs:
            minor_locs = [
                loc for loc, tr_loc in zip(minor_locs, tr_minor_locs)
                if ~np.isclose(tr_loc, tr_major_locs, atol=tol, rtol=0).any()]
        return minor_locs
