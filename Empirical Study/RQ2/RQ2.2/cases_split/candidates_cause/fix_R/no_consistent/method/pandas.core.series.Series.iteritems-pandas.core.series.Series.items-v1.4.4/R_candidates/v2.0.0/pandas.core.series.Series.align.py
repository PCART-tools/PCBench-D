    @doc(
        NDFrame.align,  # type: ignore[has-type]
        klass=_shared_doc_kwargs["klass"],
        axes_single_arg=_shared_doc_kwargs["axes_single_arg"],
    )
    def align(
        self,
        other: Series,
        join: AlignJoin = "outer",
        axis: Axis | None = None,
        level: Level = None,
        copy: bool | None = None,
        fill_value: Hashable = None,
        method: FillnaOptions | None = None,
        limit: int | None = None,
        fill_axis: Axis = 0,
        broadcast_axis: Axis | None = None,
    ) -> Series:
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
