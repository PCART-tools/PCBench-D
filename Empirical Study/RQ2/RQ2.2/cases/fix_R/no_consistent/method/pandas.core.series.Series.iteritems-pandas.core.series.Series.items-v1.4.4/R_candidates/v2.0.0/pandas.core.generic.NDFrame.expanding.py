    @final
    @doc(Expanding)
    def expanding(
        self,
        min_periods: int = 1,
        axis: Axis = 0,
        method: str = "single",
    ) -> Expanding:
        axis = self._get_axis_number(axis)
        return Expanding(self, min_periods=min_periods, axis=axis, method=method)
