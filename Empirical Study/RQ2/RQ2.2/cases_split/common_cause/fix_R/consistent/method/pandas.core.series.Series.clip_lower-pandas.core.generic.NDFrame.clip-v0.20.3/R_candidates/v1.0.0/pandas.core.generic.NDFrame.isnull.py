    @Appender(_shared_docs["isna"] % _shared_doc_kwargs)
    def isnull(self: FrameOrSeries) -> FrameOrSeries:
        return isna(self).__finalize__(self)
