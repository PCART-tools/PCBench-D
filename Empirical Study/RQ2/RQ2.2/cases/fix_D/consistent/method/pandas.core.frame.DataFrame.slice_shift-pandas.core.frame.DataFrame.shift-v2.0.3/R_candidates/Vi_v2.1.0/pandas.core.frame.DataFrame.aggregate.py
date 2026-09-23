    @doc(
        _shared_docs["aggregate"],
        klass=_shared_doc_kwargs["klass"],
        axis=_shared_doc_kwargs["axis"],
        see_also=_agg_see_also_doc,
        examples=_agg_examples_doc,
    )
    def aggregate(self, func=None, axis: Axis = 0, *args, **kwargs):
        from pandas.core.apply import frame_apply

        axis = self._get_axis_number(axis)

        op = frame_apply(self, func=func, axis=axis, args=args, kwargs=kwargs)
        result = op.agg()
        result = reconstruct_and_relabel_result(result, func, **kwargs)
        return result
