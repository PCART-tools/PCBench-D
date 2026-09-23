    @doc(
        _shared_docs["transform"],
        klass=_shared_doc_kwargs["klass"],
        axis=_shared_doc_kwargs["axis"],
    )
    def transform(
        self, func: AggFuncType, axis: Axis = 0, *args, **kwargs
    ) -> DataFrame | Series:
        # Validate axis argument
        self._get_axis_number(axis)
        result = SeriesApply(
            self, func=func, convert_dtype=True, args=args, kwargs=kwargs
        ).transform()
        return result
