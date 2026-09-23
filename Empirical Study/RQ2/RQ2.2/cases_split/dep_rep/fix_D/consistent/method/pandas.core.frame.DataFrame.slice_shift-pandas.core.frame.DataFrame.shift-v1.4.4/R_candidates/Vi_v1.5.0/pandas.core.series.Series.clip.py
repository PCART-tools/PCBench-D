    @deprecate_nonkeyword_arguments(
        version=None, allowed_args=["self", "lower", "upper"]
    )
    def clip(
        self: Series,
        lower=None,
        upper=None,
        axis: Axis | None = None,
        inplace: bool = False,
        *args,
        **kwargs,
    ) -> Series | None:
        return super().clip(lower, upper, axis, inplace, *args, **kwargs)
