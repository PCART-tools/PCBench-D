    @Appender(_agg_doc)
    @Substitution(name="rolling")
    @Appender(_shared_docs["kurt"])
    def kurt(self, **kwargs):
        return super().kurt(**kwargs)
