    def where(
        self,
        cond,
        other=lib.no_default,
        *,
        inplace: bool = False,
        axis: Axis | None = None,
        level: Level = None,
    ) -> DataFrame | None:
        return super().where(
            cond,
            other,
            inplace=inplace,
            axis=axis,
            level=level,
        )
