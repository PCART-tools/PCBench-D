    def _convert_tolerance(self, tolerance, target):
        tolerance = np.asarray(tolerance)
        if target.size != tolerance.size and tolerance.size > 1:
            raise ValueError("list-like tolerance size must match target index size")
        if not np.issubdtype(tolerance.dtype, np.number):
            if tolerance.ndim > 0:
                raise ValueError(
                    f"tolerance argument for {type(self).__name__} must contain "
                    "numeric elements if it is list type"
                )
            else:
                raise ValueError(
                    f"tolerance argument for {type(self).__name__} must be numeric "
                    f"if it is a scalar: {repr(tolerance)}"
                )
        return tolerance
