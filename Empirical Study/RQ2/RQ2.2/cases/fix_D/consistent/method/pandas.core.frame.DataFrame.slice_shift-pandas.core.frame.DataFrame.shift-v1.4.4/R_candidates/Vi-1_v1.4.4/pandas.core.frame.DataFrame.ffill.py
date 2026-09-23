    @deprecate_nonkeyword_arguments(version=None, allowed_args=["self"])
    def ffill(
        self: DataFrame,
        axis: None | Axis = None,
        inplace: bool = False,
        limit: None | int = None,
        downcast=None,
    ) -> DataFrame | None:
        return super().ffill(axis, inplace, limit, downcast)
