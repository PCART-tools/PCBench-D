    def _is_sorted(self, x):
        """Return whether x is sorted in ascending order."""
        # We don't handle the monotonically decreasing case.
        return _path.is_sorted(x)
