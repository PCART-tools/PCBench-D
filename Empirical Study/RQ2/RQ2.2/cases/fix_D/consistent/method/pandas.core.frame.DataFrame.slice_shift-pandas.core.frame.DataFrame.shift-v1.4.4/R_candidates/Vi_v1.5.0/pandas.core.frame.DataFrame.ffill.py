    @deprecate_nonkeyword_arguments(version=None, allowed_args=["self"])
    def ffill(  # type: ignore[override]
        self,
        axis: None | Axis = None,
        inplace: bool = False,
        limit: None | int = None,
        downcast: dict | None = None,
    ) -> DataFrame | None:
        return super().ffill(axis=axis, inplace=inplace, limit=limit, downcast=downcast)
