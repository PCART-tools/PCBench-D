    @deprecate_nonkeyword_arguments(version=None, allowed_args=["self", "method"])
    def interpolate(
        self: DataFrame,
        method: str = "linear",
        axis: Axis = 0,
        limit: int | None = None,
        inplace: bool = False,
        limit_direction: str | None = None,
        limit_area: str | None = None,
        downcast: str | None = None,
        **kwargs,
    ) -> DataFrame | None:
        return super().interpolate(
            method,
            axis,
            limit,
            inplace,
            limit_direction,
            limit_area,
            downcast,
            **kwargs,
        )
