    @doc(NDFrame.asfreq, **_shared_doc_kwargs)  # type: ignore[has-type]
    def asfreq(
        self,
        freq: Frequency,
        method: FillnaOptions | None = None,
        how: str | None = None,
        normalize: bool = False,
        fill_value: Hashable = None,
    ) -> Series:
        return super().asfreq(
            freq=freq,
            method=method,
            how=how,
            normalize=normalize,
            fill_value=fill_value,
        )
