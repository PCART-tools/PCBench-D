    @Substitution(
        see_also=_agg_see_also_doc,
        examples=_agg_examples_doc,
        versionadded="",
        klass="Series/Dataframe",
        axis="",
    )
    @Appender(_shared_docs["aggregate"])
    def aggregate(self, func, *args, **kwargs):
        return super().aggregate(func, *args, **kwargs)
