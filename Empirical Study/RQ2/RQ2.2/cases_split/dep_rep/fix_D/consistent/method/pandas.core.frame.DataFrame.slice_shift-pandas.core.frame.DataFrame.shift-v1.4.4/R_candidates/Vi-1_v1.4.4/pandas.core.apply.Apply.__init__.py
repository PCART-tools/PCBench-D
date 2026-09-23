    def __init__(
        self,
        obj: AggObjType,
        func,
        raw: bool,
        result_type: str | None,
        args,
        kwargs,
    ):
        self.obj = obj
        self.raw = raw
        self.args = args or ()
        self.kwargs = kwargs or {}

        if result_type not in [None, "reduce", "broadcast", "expand"]:
            raise ValueError(
                "invalid value for result_type, must be one "
                "of {None, 'reduce', 'broadcast', 'expand'}"
            )

        self.result_type = result_type

        # curry if needed
        if (
            (kwargs or args)
            and not isinstance(func, (np.ufunc, str))
            and not is_list_like(func)
        ):

            def f(x):
                return func(x, *args, **kwargs)

        else:
            f = func

        self.orig_f: AggFuncType = func
        self.f: AggFuncType = f
