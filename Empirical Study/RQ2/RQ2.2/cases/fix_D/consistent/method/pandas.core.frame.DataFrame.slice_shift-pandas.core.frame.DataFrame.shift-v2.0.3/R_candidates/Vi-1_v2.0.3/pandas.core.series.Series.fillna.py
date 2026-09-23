    @doc(NDFrame.fillna, **_shared_doc_kwargs)
    def fillna(
        self,
        value: Hashable | Mapping | Series | DataFrame = None,
        *,
        method: FillnaOptions | None = None,
        axis: Axis | None = None,
        inplace: bool = False,
        limit: int | None = None,
        downcast: dict | None = None,
    ) -> Series | None:
        return super().fillna(
            value=value,
            method=method,
            axis=axis,
            inplace=inplace,
            limit=limit,
            downcast=downcast,
        )
