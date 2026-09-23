    @Appender(generic._shared_docs["shift"] % _shared_doc_kwargs)
    def shift(self, periods=1, freq=None, axis=0, fill_value=None):
        return super().shift(
            periods=periods, freq=freq, axis=axis, fill_value=fill_value
        )
