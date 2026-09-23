    def apply(
        self,
        func: Callable[..., Any],
        raw: bool = False,
        engine: str | None = None,
        engine_kwargs: dict[str, bool] | None = None,
        args: tuple[Any, ...] | None = None,
        kwargs: dict[str, Any] | None = None,
    ):
        if args is None:
            args = ()
        if kwargs is None:
            kwargs = {}

        if not is_bool(raw):
            raise ValueError("raw parameter must be `True` or `False`")

        numba_cache_key = None
        numba_args: tuple[Any, ...] = ()
        if maybe_use_numba(engine):
            if raw is False:
                raise ValueError("raw must be `True` when using the numba engine")
            caller_name = type(self).__name__
            numba_args = args
            if self.method == "single":
                apply_func = generate_numba_apply_func(
                    kwargs, func, engine_kwargs, caller_name
                )
                numba_cache_key = (func, f"{caller_name}_apply_single")
            else:
                apply_func = generate_numba_table_func(
                    kwargs, func, engine_kwargs, f"{caller_name}_apply"
                )
                numba_cache_key = (func, f"{caller_name}_apply_table")
        elif engine in ("cython", None):
            if engine_kwargs is not None:
                raise ValueError("cython engine does not accept engine_kwargs")
            apply_func = self._generate_cython_apply_func(args, kwargs, raw, func)
        else:
            raise ValueError("engine must be either 'numba' or 'cython'")

        return self._apply(
            apply_func,
            numba_cache_key=numba_cache_key,
            numba_args=numba_args,
        )
