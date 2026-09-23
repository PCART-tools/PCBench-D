    @doc(NDFrame.asfreq, **_shared_doc_kwargs)
    def asfreq(
        self,
        freq: Frequency,
        method=None,
        how: str | None = None,
        normalize: bool = False,
        fill_value=None,
    ) -> DataFrame:
        return super().asfreq(
            freq=freq,
            method=method,
            how=how,
            normalize=normalize,
            fill_value=fill_value,
        )
