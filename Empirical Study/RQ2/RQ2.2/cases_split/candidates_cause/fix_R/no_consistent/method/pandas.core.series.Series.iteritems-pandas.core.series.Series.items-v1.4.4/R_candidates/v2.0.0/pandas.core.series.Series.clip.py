    def clip(
        self: Series,
        lower=None,
        upper=None,
        *,
        axis: Axis | None = None,
        inplace: bool = False,
        **kwargs,
    ) -> Series | None:
        return super().clip(lower, upper, axis=axis, inplace=inplace, **kwargs)
