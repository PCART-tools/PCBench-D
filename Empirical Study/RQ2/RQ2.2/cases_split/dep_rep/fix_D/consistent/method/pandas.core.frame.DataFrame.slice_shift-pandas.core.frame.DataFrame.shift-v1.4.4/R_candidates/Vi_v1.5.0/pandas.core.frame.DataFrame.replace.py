    @deprecate_nonkeyword_arguments(
        version=None, allowed_args=["self", "to_replace", "value"]
    )
    @doc(NDFrame.replace, **_shared_doc_kwargs)
    def replace(  # type: ignore[override]
        self,
        to_replace=None,
        value=lib.no_default,
        inplace: bool = False,
        limit: int | None = None,
        regex: bool = False,
        method: Literal["pad", "ffill", "bfill"] | lib.NoDefault = lib.no_default,
    ) -> DataFrame | None:
        return super().replace(
            to_replace=to_replace,
            value=value,
            inplace=inplace,
            limit=limit,
            regex=regex,
            method=method,
        )
