    @doc(
        _shared_docs["aggregate"],
        klass=_shared_doc_kwargs["klass"],
        axis=_shared_doc_kwargs["axis"],
        see_also=_agg_summary_and_see_also_doc,
        examples=_agg_examples_doc,
    )
    def aggregate(self, func=None, axis: Axis = 0, *args, **kwargs):
        from pandas.core.apply import frame_apply

        axis = self._get_axis_number(axis)

        relabeling, func, columns, order = reconstruct_func(func, **kwargs)

        op = frame_apply(self, func=func, axis=axis, args=args, kwargs=kwargs)
        result = op.agg()

        if relabeling:
            # This is to keep the order to columns occurrence unchanged, and also
            # keep the order of new columns occurrence unchanged

            # For the return values of reconstruct_func, if relabeling is
            # False, columns and order will be None.
            assert columns is not None
            assert order is not None

            result_in_dict = relabel_result(result, func, columns, order)
            result = DataFrame(result_in_dict, index=columns)

        return result
