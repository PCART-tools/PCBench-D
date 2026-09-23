    def __init__(
        self,
        obj: Series,
        func: AggFuncType,
        *,
        convert_dtype: bool | lib.NoDefault = lib.no_default,
        by_row: Literal[False, "compat", "_compat"] = "compat",
        args,
        kwargs,
    ) -> None:
        if convert_dtype is lib.no_default:
            convert_dtype = True
        else:
            warnings.warn(
                "the convert_dtype parameter is deprecated and will be removed in a "
                "future version.  Do ``ser.astype(object).apply()`` "
                "instead if you want ``convert_dtype=False``.",
                FutureWarning,
                stacklevel=find_stack_level(),
            )
        self.convert_dtype = convert_dtype

        super().__init__(
            obj,
            func,
            raw=False,
            result_type=None,
            by_row=by_row,
            args=args,
            kwargs=kwargs,
        )
