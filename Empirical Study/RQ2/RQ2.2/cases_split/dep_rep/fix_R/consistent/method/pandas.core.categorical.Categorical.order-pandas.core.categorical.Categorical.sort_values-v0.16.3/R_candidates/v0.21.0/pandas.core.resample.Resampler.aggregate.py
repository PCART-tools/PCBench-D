    @Appender(_agg_doc)
    @Appender(_shared_docs['aggregate'] % dict(
        klass='DataFrame',
        versionadded=''))
    def aggregate(self, arg, *args, **kwargs):

        self._set_binner()
        result, how = self._aggregate(arg, *args, **kwargs)
        if result is None:
            result = self._groupby_and_aggregate(arg,
                                                 *args,
                                                 **kwargs)

        result = self._apply_loffset(result)
        return result
