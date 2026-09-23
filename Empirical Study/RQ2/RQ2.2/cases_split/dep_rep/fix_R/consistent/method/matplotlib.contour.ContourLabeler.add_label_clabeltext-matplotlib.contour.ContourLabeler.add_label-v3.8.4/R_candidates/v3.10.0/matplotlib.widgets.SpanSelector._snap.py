    @staticmethod
    def _snap(values, snap_values):
        """Snap values to a given array values (snap_values)."""
        # take into account machine precision
        eps = np.min(np.abs(np.diff(snap_values))) * 1e-12
        return tuple(
            snap_values[np.abs(snap_values - v + np.sign(v) * eps).argmin()]
            for v in values)
