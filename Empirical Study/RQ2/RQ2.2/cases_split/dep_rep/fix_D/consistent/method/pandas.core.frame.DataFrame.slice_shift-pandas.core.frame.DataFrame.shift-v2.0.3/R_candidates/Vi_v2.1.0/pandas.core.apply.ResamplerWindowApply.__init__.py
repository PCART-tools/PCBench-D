    def __init__(
        self,
        obj: Resampler | BaseWindow,
        func: AggFuncType,
        *,
        args,
        kwargs,
    ) -> None:
        super(GroupByApply, self).__init__(
            obj,
            func,
            raw=False,
            result_type=None,
            args=args,
            kwargs=kwargs,
        )
