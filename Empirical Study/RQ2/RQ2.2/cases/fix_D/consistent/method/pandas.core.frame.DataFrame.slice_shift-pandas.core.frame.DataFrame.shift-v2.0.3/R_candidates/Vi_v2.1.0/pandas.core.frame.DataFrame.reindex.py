    @doc(
        NDFrame.reindex,
        klass=_shared_doc_kwargs["klass"],
        optional_reindex=_shared_doc_kwargs["optional_reindex"],
    )
    def reindex(
        self,
        labels=None,
        *,
        index=None,
        columns=None,
        axis: Axis | None = None,
        method: ReindexMethod | None = None,
        copy: bool | None = None,
        level: Level | None = None,
        fill_value: Scalar | None = np.nan,
        limit: int | None = None,
        tolerance=None,
    ) -> DataFrame:
        return super().reindex(
            labels=labels,
            index=index,
            columns=columns,
            axis=axis,
            method=method,
            copy=copy,
            level=level,
            fill_value=fill_value,
            limit=limit,
            tolerance=tolerance,
        )
