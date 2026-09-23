    @doc(NDFrame.align, **_shared_doc_kwargs)
    def align(
        self,
        other: DataFrame,
        join: Literal["outer", "inner", "left", "right"] = "outer",
        axis: Axis | None = None,
        level: Level = None,
        copy: bool = True,
        fill_value=None,
        method: FillnaOptions | None = None,
        limit: int | None = None,
        fill_axis: Axis = 0,
        broadcast_axis: Axis | None = None,
    ) -> DataFrame:
        return super().align(
            other,
            join=join,
            axis=axis,
            level=level,
            copy=copy,
            fill_value=fill_value,
            method=method,
            limit=limit,
            fill_axis=fill_axis,
            broadcast_axis=broadcast_axis,
        )
