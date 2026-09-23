    @doc(NDFrame.asfreq, **_shared_doc_kwargs)
    def asfreq(
        self,
        freq: Frequency,
        method: FillnaOptions | None = None,
        how: str | None = None,
        normalize: bool = False,
        fill_value: Hashable = None,
    ) -> DataFrame:
        return super().asfreq(
            freq=freq,
            method=method,
            how=how,
            normalize=normalize,
            fill_value=fill_value,
        )
