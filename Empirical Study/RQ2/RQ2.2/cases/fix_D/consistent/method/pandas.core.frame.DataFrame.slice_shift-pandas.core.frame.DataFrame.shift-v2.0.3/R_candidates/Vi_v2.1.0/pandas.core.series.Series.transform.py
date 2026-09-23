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
        ser = self.copy(deep=False) if using_copy_on_write() else self
        result = SeriesApply(ser, func=func, args=args, kwargs=kwargs).transform()
        return result
