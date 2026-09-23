    @Appender(_shared_docs["isna"] % _shared_doc_kwargs)
    def isna(self: FrameOrSeries) -> FrameOrSeries:
        return isna(self).__finalize__(self)
