    @Substitution(
        see_also=_agg_see_also_doc,
        examples=_agg_examples_doc,
        versionadded="",
        klass="DataFrame",
        axis="",
    )
    @Appender(_shared_docs["aggregate"])
    def aggregate(self, func, *args, **kwargs):

        self._set_binner()
        result, how = self._aggregate(func, *args, **kwargs)
        if result is None:
            how = func
            grouper = None
            result = self._groupby_and_aggregate(how, grouper, *args, **kwargs)

        result = self._apply_loffset(result)
        return result
