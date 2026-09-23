    def _convert_tolerance(self, tolerance, target: np.ndarray | Index) -> np.ndarray:
        # override this method on subclasses
        tolerance = np.asarray(tolerance)
        if target.size != tolerance.size and tolerance.size > 1:
            raise ValueError("list-like tolerance size must match target index size")
        return tolerance
