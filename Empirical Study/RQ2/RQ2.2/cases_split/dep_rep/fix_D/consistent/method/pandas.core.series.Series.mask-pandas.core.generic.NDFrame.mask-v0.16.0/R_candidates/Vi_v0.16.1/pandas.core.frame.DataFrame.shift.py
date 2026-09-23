    @Appender(_shared_docs['shift'] % _shared_doc_kwargs)
    def shift(self, periods=1, freq=None, axis=0, **kwargs):
        return super(DataFrame, self).shift(periods=periods, freq=freq,
                                            axis=axis, **kwargs)
