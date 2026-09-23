    def searchsorted(self, v, side="left", sorter=None):
        msg = "searchsorted requires high memory usage."
        warnings.warn(msg, PerformanceWarning, stacklevel=2)
        if not is_scalar(v):
            v = np.asarray(v)
        v = np.asarray(v)
        return np.asarray(self, dtype=self.dtype.subtype).searchsorted(
            v, side, sorter
        )
