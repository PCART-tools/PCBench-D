    def bfill(
        self,
        *,
        axis: None | Axis = None,
        inplace: bool = False,
        limit: None | int = None,
        downcast=None,
    ) -> DataFrame | None:
        return super().bfill(axis=axis, inplace=inplace, limit=limit, downcast=downcast)
