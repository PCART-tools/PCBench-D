    @doc(
        _shared_docs["transform"],
        klass=_shared_doc_kwargs["klass"],
        axis=_shared_doc_kwargs["axis"],
    )
    def transform(
        self, func: AggFuncType, axis: Axis = 0, *args, **kwargs
    ) -> DataFrame:
        from pandas.core.apply import frame_apply

        op = frame_apply(self, func=func, axis=axis, args=args, kwargs=kwargs)
        result = op.transform()
        assert isinstance(result, DataFrame)
        return result
