    def _convert_tolerance(self, tolerance, target):
        tolerance = super()._convert_tolerance(tolerance, target)

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
