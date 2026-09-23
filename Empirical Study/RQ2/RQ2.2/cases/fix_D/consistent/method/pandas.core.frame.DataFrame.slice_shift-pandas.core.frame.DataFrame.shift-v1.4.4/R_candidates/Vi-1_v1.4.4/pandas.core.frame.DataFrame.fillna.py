    @deprecate_nonkeyword_arguments(version=None, allowed_args=["self", "value"])
    @doc(NDFrame.fillna, **_shared_doc_kwargs)
    def fillna(
        self,
        value: object | ArrayLike | None = None,
        method: FillnaOptions | None = None,
        axis: Axis | None = None,
        inplace: bool = False,
        limit=None,
        downcast=None,
    ) -> DataFrame | None:
        return super().fillna(
            value=value,
            method=method,
            axis=axis,
            inplace=inplace,
            limit=limit,
            downcast=downcast,
        )
