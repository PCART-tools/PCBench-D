    def clip(
        self: DataFrame,
        lower: float | None = None,
        upper: float | None = None,
        *,
        axis: Axis | None = None,
        inplace: bool = False,
        **kwargs,
    ) -> DataFrame | None:
        return super().clip(lower, upper, axis=axis, inplace=inplace, **kwargs)
