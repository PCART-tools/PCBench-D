    def bfill(
        self,
        *,
        axis: None | Axis = None,
        inplace: bool = False,
        limit: None | int = None,
        downcast: dict | None = None,
    ) -> Series | None:
        return super().bfill(axis=axis, inplace=inplace, limit=limit, downcast=downcast)
