    @deprecate_nonkeyword_arguments(version=None, allowed_args=["self"])
    def bfill(
        self: Series,
        axis: None | Axis = None,
        inplace: bool = False,
        limit: None | int = None,
        downcast=None,
    ) -> Series | None:
        return super().bfill(axis, inplace, limit, downcast)
