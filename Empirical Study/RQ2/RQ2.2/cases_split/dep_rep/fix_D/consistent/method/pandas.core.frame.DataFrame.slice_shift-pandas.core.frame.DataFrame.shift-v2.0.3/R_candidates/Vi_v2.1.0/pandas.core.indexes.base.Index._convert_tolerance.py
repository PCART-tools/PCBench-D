    def _convert_tolerance(self, tolerance, target: np.ndarray | Index) -> np.ndarray:
        # override this method on subclasses
        tolerance = np.asarray(tolerance)
        if target.size != tolerance.size and tolerance.size > 1:
            raise ValueError("list-like tolerance size must match target index size")
        elif is_numeric_dtype(self) and not np.issubdtype(tolerance.dtype, np.number):
            if tolerance.ndim > 0:
                raise ValueError(
                    f"tolerance argument for {type(self).__name__} with dtype "
                    f"{self.dtype} must contain numeric elements if it is list type"
                )

            raise ValueError(
                f"tolerance argument for {type(self).__name__} with dtype {self.dtype} "
                f"must be numeric if it is a scalar: {repr(tolerance)}"
            )
        return tolerance
