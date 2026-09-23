    @deprecate_nonkeyword_arguments(version=None, allowed_args=["self"])
    def bfill(  # type: ignore[override]
        self,
        axis: None | Axis = None,
        inplace: bool = False,
        limit: None | int = None,
        downcast=None,
    ) -> DataFrame | None:
        return super().bfill(axis=axis, inplace=inplace, limit=limit, downcast=downcast)
