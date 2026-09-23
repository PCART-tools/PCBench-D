    def _is_sorted(self, x):
        """return True if x is sorted in ascending order"""
        # We don't handle the monotonically decreasing case.
        return _path.is_sorted(x)
