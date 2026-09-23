    def __init__(
        self,
        obj: Series,
        func: AggFuncType,
        convert_dtype: bool,
        args,
        kwargs,
    ):
        self.convert_dtype = convert_dtype

        super().__init__(
            obj,
            func,
            raw=False,
            result_type=None,
            args=args,
            kwargs=kwargs,
        )
