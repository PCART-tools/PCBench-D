    @doc(
        NDFrame.reindex,  # type: ignore[has-type]
        klass=_shared_doc_kwargs["klass"],
        optional_reindex=_shared_doc_kwargs["optional_reindex"],
    )
    def reindex(  # type: ignore[override]
        self,
        index=None,
        *,
        axis: Axis | None = None,
        method: ReindexMethod | None = None,
        copy: bool | None = None,
        level: Level | None = None,
        fill_value: Scalar | None = None,
        limit: int | None = None,
        tolerance=None,
    ) -> Series:
        return super().reindex(
            index=index,
            method=method,
            copy=copy,
            level=level,
            fill_value=fill_value,
            limit=limit,
            tolerance=tolerance,
        )
