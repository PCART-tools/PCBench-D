    @Substitution(
        see_also=_agg_summary_and_see_also_doc,
        examples=_agg_examples_doc,
        versionadded="\n.. versionadded:: 0.20.0\n",
        **_shared_doc_kwargs,
    )
    @Appender(_shared_docs["aggregate"])
    def aggregate(self, func, axis=0, *args, **kwargs):
        axis = self._get_axis_number(axis)

        result = None
        try:
            result, how = self._aggregate(func, axis=axis, *args, **kwargs)
        except TypeError:
            pass
        if result is None:
            return self.apply(func, axis=axis, args=args, **kwargs)
        return result
