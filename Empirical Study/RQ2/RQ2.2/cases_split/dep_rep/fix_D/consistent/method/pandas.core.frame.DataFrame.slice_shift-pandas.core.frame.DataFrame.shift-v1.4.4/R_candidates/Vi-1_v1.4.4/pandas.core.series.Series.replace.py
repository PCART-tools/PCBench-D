    @doc(
        NDFrame.replace,  # type: ignore[has-type]
        klass=_shared_doc_kwargs["klass"],
        inplace=_shared_doc_kwargs["inplace"],
        replace_iloc=_shared_doc_kwargs["replace_iloc"],
    )
    def replace(
        self,
        to_replace=None,
        value=lib.no_default,
        inplace=False,
        limit=None,
        regex=False,
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
