    @doc(NDFrame.replace, **_shared_doc_kwargs)
    def replace(
        self,
        to_replace=None,
        value=lib.no_default,
        inplace: bool = False,
        limit=None,
        regex: bool = False,
        method: str | lib.NoDefault = lib.no_default,
    ):
        return super().replace(
            to_replace=to_replace,
            value=value,
            inplace=inplace,
            limit=limit,
            regex=regex,
            method=method,
        )
