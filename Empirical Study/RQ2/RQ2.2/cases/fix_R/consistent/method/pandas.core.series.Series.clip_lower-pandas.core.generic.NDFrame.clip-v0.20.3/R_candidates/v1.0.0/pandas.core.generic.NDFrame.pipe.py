    @Appender(_shared_docs["pipe"] % _shared_doc_kwargs)
    def pipe(self, func, *args, **kwargs):
        return com.pipe(self, func, *args, **kwargs)
