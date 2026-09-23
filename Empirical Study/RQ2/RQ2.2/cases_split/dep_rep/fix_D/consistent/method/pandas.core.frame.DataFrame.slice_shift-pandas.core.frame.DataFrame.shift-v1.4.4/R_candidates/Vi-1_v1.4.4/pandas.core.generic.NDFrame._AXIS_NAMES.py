    @property
    def _AXIS_NAMES(self) -> dict[int, str]:
        """.. deprecated:: 1.1.0"""
        level = self.ndim + 1
        warnings.warn(
            "_AXIS_NAMES has been deprecated.", FutureWarning, stacklevel=level
        )
        return {0: "index"}
