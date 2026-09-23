    @Appender(_agg_doc)
    @Appender(_shared_docs['aggregate'] % dict(
        versionadded='',
        klass='Series/DataFrame'))
    def aggregate(self, arg, *args, **kwargs):
        result, how = self._aggregate(arg, *args, **kwargs)
        if result is None:

            # these must apply directly
            result = arg(self)

        return result
