    def __init__(
        self,
        obj: NDFrame,
        min_periods: int = 1,
        center=None,
        axis: Axis = 0,
        method: str = "single",
        selection=None,
    ):
        super().__init__(
            obj=obj,
            min_periods=min_periods,
            center=center,
            axis=axis,
            method=method,
            selection=selection,
        )
