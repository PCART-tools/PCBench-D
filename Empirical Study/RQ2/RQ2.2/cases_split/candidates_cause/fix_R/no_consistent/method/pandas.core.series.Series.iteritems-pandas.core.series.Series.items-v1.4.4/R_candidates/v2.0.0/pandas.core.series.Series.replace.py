    @doc(
        NDFrame.replace,
        klass=_shared_doc_kwargs["klass"],
        inplace=_shared_doc_kwargs["inplace"],
        replace_iloc=_shared_doc_kwargs["replace_iloc"],
    )
    def replace(
        self,
        to_replace=None,
        value=lib.no_default,
        *,
        inplace: bool = False,
        limit: int | None = None,
        regex: bool = False,
        method: Literal["pad", "ffill", "bfill"] | lib.NoDefault = lib.no_default,
    ) -> Series | None:
        return super().replace(
            to_replace=to_replace,
            value=value,
            inplace=inplace,
            limit=limit,
            regex=regex,
            method=method,
        )
