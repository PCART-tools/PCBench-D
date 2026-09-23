    @property
    def _AXIS_NAMES(self) -> dict[int, str]:
        """.. deprecated:: 1.1.0"""
        super()._AXIS_NAMES
        return {0: "index", 1: "columns"}
