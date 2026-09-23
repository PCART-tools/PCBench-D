    @deprecate_nonkeyword_arguments(version=None, allowed_args=["self", "value"])
    @doc(NDFrame.fillna, **_shared_doc_kwargs)  # type: ignore[has-type]
    def fillna(
        self,
        value: object | ArrayLike | None = None,
        method: FillnaOptions | None = None,
        axis=None,
        inplace=False,
        limit=None,
        downcast=None,
    ) -> Series | None:
        return super().fillna(
            value=value,
            method=method,
            axis=axis,
            inplace=inplace,
            limit=limit,
            downcast=downcast,
        )
