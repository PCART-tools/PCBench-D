    @Substitution(see_also=_agg_see_also_doc,
                  examples=_agg_examples_doc,
                  versionadded='',
                  klass='Series/DataFrame',
                  axis='')
    @Appender(_shared_docs['aggregate'])
    def aggregate(self, arg, *args, **kwargs):
        result, how = self._aggregate(arg, *args, **kwargs)
        if result is None:

            # these must apply directly
            result = arg(self)

        return result
