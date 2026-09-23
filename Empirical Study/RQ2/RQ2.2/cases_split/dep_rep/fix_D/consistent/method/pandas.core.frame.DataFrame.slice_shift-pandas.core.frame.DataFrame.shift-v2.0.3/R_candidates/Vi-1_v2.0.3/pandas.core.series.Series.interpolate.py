    def interpolate(
        self: Series,
        method: str = "linear",
        *,
        axis: Axis = 0,
        limit: int | None = None,
        inplace: bool = False,
        limit_direction: str | None = None,
        limit_area: str | None = None,
        downcast: str | None = None,
        **kwargs,
    ) -> Series | None:
        return super().interpolate(
            method=method,
            axis=axis,
            limit=limit,
            inplace=inplace,
            limit_direction=limit_direction,
            limit_area=limit_area,
            downcast=downcast,
            **kwargs,
        )
