    def __init__(
        self,
        obj: "DataFrame",
        func,
        raw: bool,
        result_type,
        ignore_failures: bool,
        args,
        kwds,
    ):
        self.obj = obj
        self.raw = raw
        self.ignore_failures = ignore_failures
        self.args = args or ()
        self.kwds = kwds or {}

        if result_type not in [None, "reduce", "broadcast", "expand"]:
            raise ValueError(
                "invalid value for result_type, must be one "
                "of {None, 'reduce', 'broadcast', 'expand'}"
            )

        self.result_type = result_type

        # curry if needed
        if (kwds or args) and not isinstance(func, (np.ufunc, str)):

            def f(x):
                return func(x, *args, **kwds)

        else:
            f = func

        self.f = f
