    @Substitution(
        see_also=_agg_see_also_doc,
        examples=_agg_examples_doc,
        versionadded="",
        klass="DataFrame",
        axis="",
    )
    @Appender(_shared_docs["aggregate"])
    def aggregate(self, arg=None, *args, **kwargs):
        return super().aggregate(arg, *args, **kwargs)
