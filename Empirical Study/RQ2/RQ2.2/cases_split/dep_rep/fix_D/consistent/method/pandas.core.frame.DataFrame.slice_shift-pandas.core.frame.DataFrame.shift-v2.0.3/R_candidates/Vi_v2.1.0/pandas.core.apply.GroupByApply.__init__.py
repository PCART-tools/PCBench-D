    def __init__(
        self,
        obj: GroupBy[NDFrameT],
        func: AggFuncType,
        *,
        args,
        kwargs,
    ) -> None:
        kwargs = kwargs.copy()
        self.axis = obj.obj._get_axis_number(kwargs.get("axis", 0))
        super().__init__(
            obj,
            func,
            raw=False,
            result_type=None,
            args=args,
            kwargs=kwargs,
        )
