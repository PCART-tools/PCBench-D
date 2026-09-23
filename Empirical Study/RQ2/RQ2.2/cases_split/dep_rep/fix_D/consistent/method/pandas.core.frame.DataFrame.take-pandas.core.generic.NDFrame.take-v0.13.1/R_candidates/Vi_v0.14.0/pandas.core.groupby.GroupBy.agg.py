    @Appender(_agg_doc)
    def agg(self, func, *args, **kwargs):
        return self.aggregate(func, *args, **kwargs)
