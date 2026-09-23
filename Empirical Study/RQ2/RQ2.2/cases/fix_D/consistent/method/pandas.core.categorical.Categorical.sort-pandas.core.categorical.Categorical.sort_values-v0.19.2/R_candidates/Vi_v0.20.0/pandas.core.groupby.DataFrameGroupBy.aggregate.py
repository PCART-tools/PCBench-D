    @Appender(_agg_doc)
    @Appender(_shared_docs['aggregate'] % dict(
        klass='DataFrame',
        versionadded=''))
    def aggregate(self, arg, *args, **kwargs):
        return super(DataFrameGroupBy, self).aggregate(arg, *args, **kwargs)
