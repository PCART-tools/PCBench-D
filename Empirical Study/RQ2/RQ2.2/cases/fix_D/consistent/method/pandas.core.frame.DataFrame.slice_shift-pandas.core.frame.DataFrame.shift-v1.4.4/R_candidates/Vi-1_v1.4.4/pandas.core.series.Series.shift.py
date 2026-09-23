    @doc(NDFrame.shift, klass=_shared_doc_kwargs["klass"])  # type: ignore[has-type]
    def shift(self, periods=1, freq=None, axis=0, fill_value=None) -> Series:
        return super().shift(
            periods=periods, freq=freq, axis=axis, fill_value=fill_value
        )
