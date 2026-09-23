    def _convert_tolerance(self, tolerance, target):
        tolerance = np.asarray(tolerance)
        if target.size != tolerance.size and tolerance.size > 1:
            raise ValueError("list-like tolerance size must match " "target index size")
        if not np.issubdtype(tolerance.dtype, np.number):
            if tolerance.ndim > 0:
                raise ValueError(
                    (
                        "tolerance argument for %s must contain "
                        "numeric elements if it is list type"
                    )
                    % (type(self).__name__,)
                )
            else:
                raise ValueError(
                    (
                        "tolerance argument for %s must be numeric "
                        "if it is a scalar: %r"
                    )
                    % (type(self).__name__, tolerance)
                )
        return tolerance
