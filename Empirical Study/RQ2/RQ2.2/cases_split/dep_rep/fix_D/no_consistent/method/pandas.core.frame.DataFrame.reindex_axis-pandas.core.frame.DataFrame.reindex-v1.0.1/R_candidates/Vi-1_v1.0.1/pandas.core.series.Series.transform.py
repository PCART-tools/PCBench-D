    @Appender(generic._shared_docs["transform"] % _shared_doc_kwargs)
    def transform(self, func, axis=0, *args, **kwargs):
        # Validate the axis parameter
        self._get_axis_number(axis)
        return super().transform(func, *args, **kwargs)
