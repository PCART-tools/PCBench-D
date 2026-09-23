    @doc(
        template_header,
        create_section_header("Parameters"),
        args_compat,
        window_agg_numba_parameters(),
        kwargs_compat,
        create_section_header("Returns"),
        template_returns,
        create_section_header("See Also"),
        template_see_also,
        create_section_header("Notes"),
        numba_notes.replace("\n", "", 1),
        window_method="ewm",
        aggregation_description="(exponential weighted moment) sum",
        agg_method="sum",
    )
    def sum(self, *args, engine=None, engine_kwargs=None, **kwargs):
        if not self.adjust:
            raise NotImplementedError("sum is not implemented with adjust=False")
        if maybe_use_numba(engine):
            if self.method == "single":
                func = generate_numba_ewm_func
                numba_cache_key = (lambda x: x, "ewm_sum")
            else:
                func = generate_numba_ewm_table_func
                numba_cache_key = (lambda x: x, "ewm_sum_table")
            ewm_func = func(
                engine_kwargs=engine_kwargs,
                com=self._com,
                adjust=self.adjust,
                ignore_na=self.ignore_na,
                deltas=self._deltas,
                normalize=False,
            )
            return self._apply(
                ewm_func,
                numba_cache_key=numba_cache_key,
            )
        elif engine in ("cython", None):
            if engine_kwargs is not None:
                raise ValueError("cython engine does not accept engine_kwargs")
            nv.validate_window_func("sum", args, kwargs)

            deltas = None if self.times is None else self._deltas
            window_func = partial(
                window_aggregations.ewm,
                com=self._com,
                adjust=self.adjust,
                ignore_na=self.ignore_na,
                deltas=deltas,
                normalize=False,
            )
            return self._apply(window_func)
        else:
            raise ValueError("engine must be either 'numba' or 'cython'")
