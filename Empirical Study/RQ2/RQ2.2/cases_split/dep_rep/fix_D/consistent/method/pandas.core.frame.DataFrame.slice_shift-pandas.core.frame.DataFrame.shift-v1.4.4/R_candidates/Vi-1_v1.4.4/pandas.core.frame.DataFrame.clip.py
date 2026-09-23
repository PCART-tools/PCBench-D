    @deprecate_nonkeyword_arguments(
        version=None, allowed_args=["self", "lower", "upper"]
    )
    def clip(
        self: DataFrame,
        lower=None,
        upper=None,
        axis: Axis | None = None,
        inplace: bool = False,
        *args,
        **kwargs,
    ) -> DataFrame | None:
        return super().clip(lower, upper, axis, inplace, *args, **kwargs)
