    def mask(
        self,
        cond,
        other=lib.no_default,
        *,
        inplace: bool = False,
        axis: Axis | None = None,
        level: Level = None,
    ) -> DataFrame | None:
        return super().mask(
            cond,
            other,
            inplace=inplace,
            axis=axis,
            level=level,
        )
