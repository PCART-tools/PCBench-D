    @Substitution(
        see_also=_agg_see_also_doc,
        examples=_agg_examples_doc,
        versionadded="\n.. versionadded:: 0.20.0\n",
        **_shared_doc_kwargs,
    )
    @Appender(generic._shared_docs["aggregate"])
    def aggregate(self, func, axis=0, *args, **kwargs):
        # Validate the axis parameter
        self._get_axis_number(axis)
        result, how = self._aggregate(func, *args, **kwargs)
        if result is None:

            # we can be called from an inner function which
            # passes this meta-data
            kwargs.pop("_axis", None)
            kwargs.pop("_level", None)

            # try a regular apply, this evaluates lambdas
            # row-by-row; however if the lambda is expected a Series
            # expression, e.g.: lambda x: x-x.quantile(0.25)
            # this will fail, so we can try a vectorized evaluation

            # we cannot FIRST try the vectorized evaluation, because
            # then .agg and .apply would have different semantics if the
            # operation is actually defined on the Series, e.g. str
            try:
                result = self.apply(func, *args, **kwargs)
            except (ValueError, AttributeError, TypeError):
                result = func(self, *args, **kwargs)

        return result
