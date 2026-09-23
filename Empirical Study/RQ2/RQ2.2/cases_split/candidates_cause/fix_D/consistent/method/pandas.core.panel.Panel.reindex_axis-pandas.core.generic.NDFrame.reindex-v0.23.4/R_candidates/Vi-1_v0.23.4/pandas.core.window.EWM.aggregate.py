    @Appender(_agg_doc)
    @Appender(_shared_docs['aggregate'] % dict(
        versionadded='',
        klass='Series/DataFrame',
        axis=''))
    def aggregate(self, arg, *args, **kwargs):
        return super(EWM, self).aggregate(arg, *args, **kwargs)
