    @property
    def _AXIS_NUMBERS(self) -> dict[str, int]:
        """.. deprecated:: 1.1.0"""
        super()._AXIS_NUMBERS
        return {"index": 0, "columns": 1}
