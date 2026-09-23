    @classmethod
    def _add_numeric_operations(cls):
        """
        Add the operations to the cls; evaluate the doc strings again
        """
        axis_descr, name1, name2 = _doc_params(cls)

        @doc(
            _bool_doc,
            desc=_any_desc,
            name1=name1,
            name2=name2,
            axis_descr=axis_descr,
            see_also=_any_see_also,
            examples=_any_examples,
            empty_value=False,
        )
        def any(self, axis=0, bool_only=None, skipna=True, level=None, **kwargs):
            return NDFrame.any(self, axis, bool_only, skipna, level, **kwargs)

        setattr(cls, "any", any)

        @doc(
            _bool_doc,
            desc=_all_desc,
            name1=name1,
            name2=name2,
            axis_descr=axis_descr,
            see_also=_all_see_also,
            examples=_all_examples,
            empty_value=True,
        )
        def all(self, axis=0, bool_only=None, skipna=True, level=None, **kwargs):
            return NDFrame.all(self, axis, bool_only, skipna, level, **kwargs)

        setattr(cls, "all", all)

        # error: Argument 1 to "doc" has incompatible type "Optional[str]"; expected
        # "Union[str, Callable[..., Any]]"
        @doc(
            NDFrame.mad.__doc__,  # type: ignore[arg-type]
            desc="Return the mean absolute deviation of the values "
            "over the requested axis.",
            name1=name1,
            name2=name2,
            axis_descr=axis_descr,
            see_also="",
            examples="",
        )
        def mad(self, axis=None, skipna=True, level=None):
            return NDFrame.mad(self, axis, skipna, level)

        setattr(cls, "mad", mad)

        @doc(
            _num_ddof_doc,
            desc="Return unbiased standard error of the mean over requested "
            "axis.\n\nNormalized by N-1 by default. This can be changed "
            "using the ddof argument",
            name1=name1,
            name2=name2,
            axis_descr=axis_descr,
            notes="",
            examples="",
        )
        def sem(
            self,
            axis=None,
            skipna=True,
            level=None,
            ddof=1,
            numeric_only=None,
            **kwargs,
        ):
            return NDFrame.sem(self, axis, skipna, level, ddof, numeric_only, **kwargs)

        setattr(cls, "sem", sem)

        @doc(
            _num_ddof_doc,
            desc="Return unbiased variance over requested axis.\n\nNormalized by "
            "N-1 by default. This can be changed using the ddof argument.",
            name1=name1,
            name2=name2,
            axis_descr=axis_descr,
            notes="",
            examples=_var_examples,
        )
        def var(
            self,
            axis=None,
            skipna=True,
            level=None,
            ddof=1,
            numeric_only=None,
            **kwargs,
        ):
            return NDFrame.var(self, axis, skipna, level, ddof, numeric_only, **kwargs)

        setattr(cls, "var", var)

        @doc(
            _num_ddof_doc,
            desc="Return sample standard deviation over requested axis."
            "\n\nNormalized by N-1 by default. This can be changed using the "
            "ddof argument.",
            name1=name1,
            name2=name2,
            axis_descr=axis_descr,
            notes=_std_notes,
            examples=_std_examples,
        )
        def std(
            self,
            axis=None,
            skipna=True,
            level=None,
            ddof=1,
            numeric_only=None,
            **kwargs,
        ):
            return NDFrame.std(self, axis, skipna, level, ddof, numeric_only, **kwargs)

        setattr(cls, "std", std)

        @doc(
            _cnum_doc,
            desc="minimum",
            name1=name1,
            name2=name2,
            axis_descr=axis_descr,
            accum_func_name="min",
            examples=_cummin_examples,
        )
        def cummin(self, axis=None, skipna=True, *args, **kwargs):
            return NDFrame.cummin(self, axis, skipna, *args, **kwargs)

        setattr(cls, "cummin", cummin)

        @doc(
            _cnum_doc,
            desc="maximum",
            name1=name1,
            name2=name2,
            axis_descr=axis_descr,
            accum_func_name="max",
            examples=_cummax_examples,
        )
        def cummax(self, axis=None, skipna=True, *args, **kwargs):
            return NDFrame.cummax(self, axis, skipna, *args, **kwargs)

        setattr(cls, "cummax", cummax)

        @doc(
            _cnum_doc,
            desc="sum",
            name1=name1,
            name2=name2,
            axis_descr=axis_descr,
            accum_func_name="sum",
            examples=_cumsum_examples,
        )
        def cumsum(self, axis=None, skipna=True, *args, **kwargs):
            return NDFrame.cumsum(self, axis, skipna, *args, **kwargs)

        setattr(cls, "cumsum", cumsum)

        @doc(
            _cnum_doc,
            desc="product",
            name1=name1,
            name2=name2,
            axis_descr=axis_descr,
            accum_func_name="prod",
            examples=_cumprod_examples,
        )
        def cumprod(self, axis=None, skipna=True, *args, **kwargs):
            return NDFrame.cumprod(self, axis, skipna, *args, **kwargs)

        setattr(cls, "cumprod", cumprod)

        @doc(
            _num_doc,
            desc="Return the sum of the values over the requested axis.\n\n"
            "This is equivalent to the method ``numpy.sum``.",
            name1=name1,
            name2=name2,
            axis_descr=axis_descr,
            min_count=_min_count_stub,
            see_also=_stat_func_see_also,
            examples=_sum_examples,
        )
        def sum(
            self,
            axis=None,
            skipna=True,
            level=None,
            numeric_only=None,
            min_count=0,
            **kwargs,
        ):
            return NDFrame.sum(
                self, axis, skipna, level, numeric_only, min_count, **kwargs
            )

        setattr(cls, "sum", sum)

        @doc(
            _num_doc,
            desc="Return the product of the values over the requested axis.",
            name1=name1,
            name2=name2,
            axis_descr=axis_descr,
            min_count=_min_count_stub,
            see_also=_stat_func_see_also,
            examples=_prod_examples,
        )
        def prod(
            self,
            axis=None,
            skipna=True,
            level=None,
            numeric_only=None,
            min_count=0,
            **kwargs,
        ):
            return NDFrame.prod(
                self, axis, skipna, level, numeric_only, min_count, **kwargs
            )

        setattr(cls, "prod", prod)
        cls.product = prod

        @doc(
            _num_doc,
            desc="Return the mean of the values over the requested axis.",
            name1=name1,
            name2=name2,
            axis_descr=axis_descr,
            min_count="",
            see_also="",
            examples="",
        )
        def mean(
            self,
            axis: int | None | lib.NoDefault = lib.no_default,
            skipna=True,
            level=None,
            numeric_only=None,
            **kwargs,
        ):
            return NDFrame.mean(self, axis, skipna, level, numeric_only, **kwargs)

        setattr(cls, "mean", mean)

        @doc(
            _num_doc,
            desc="Return unbiased skew over requested axis.\n\nNormalized by N-1.",
            name1=name1,
            name2=name2,
            axis_descr=axis_descr,
            min_count="",
            see_also="",
            examples="",
        )
        def skew(
            self,
            axis: int | None | lib.NoDefault = lib.no_default,
            skipna=True,
            level=None,
            numeric_only=None,
            **kwargs,
        ):
            return NDFrame.skew(self, axis, skipna, level, numeric_only, **kwargs)

        setattr(cls, "skew", skew)

        @doc(
            _num_doc,
            desc="Return unbiased kurtosis over requested axis.\n\n"
            "Kurtosis obtained using Fisher's definition of\n"
            "kurtosis (kurtosis of normal == 0.0). Normalized "
            "by N-1.",
            name1=name1,
            name2=name2,
            axis_descr=axis_descr,
            min_count="",
            see_also="",
            examples="",
        )
        def kurt(
            self,
            axis: Axis | None | lib.NoDefault = lib.no_default,
            skipna=True,
            level=None,
            numeric_only=None,
            **kwargs,
        ):
            return NDFrame.kurt(self, axis, skipna, level, numeric_only, **kwargs)

        setattr(cls, "kurt", kurt)
        cls.kurtosis = kurt

        @doc(
            _num_doc,
            desc="Return the median of the values over the requested axis.",
            name1=name1,
            name2=name2,
            axis_descr=axis_descr,
            min_count="",
            see_also="",
            examples="",
        )
        def median(
            self,
            axis: int | None | lib.NoDefault = lib.no_default,
            skipna=True,
            level=None,
            numeric_only=None,
            **kwargs,
        ):
            return NDFrame.median(self, axis, skipna, level, numeric_only, **kwargs)

        setattr(cls, "median", median)

        # error: Untyped decorator makes function "max" untyped
        @doc(  # type: ignore[misc]
            _num_doc,
            desc="Return the maximum of the values over the requested axis.\n\n"
            "If you want the *index* of the maximum, use ``idxmax``. This is "
            "the equivalent of the ``numpy.ndarray`` method ``argmax``.",
            name1=name1,
            name2=name2,
            axis_descr=axis_descr,
            min_count="",
            see_also=_stat_func_see_also,
            examples=_max_examples,
        )
        def max(
            self,
            axis: int | None | lib.NoDefault = lib.no_default,
            skipna=True,
            level=None,
            numeric_only=None,
            **kwargs,
        ):
            return NDFrame.max(self, axis, skipna, level, numeric_only, **kwargs)

        setattr(cls, "max", max)

        # error: Untyped decorator makes function "max" untyped
        @doc(  # type: ignore[misc]
            _num_doc,
            desc="Return the minimum of the values over the requested axis.\n\n"
            "If you want the *index* of the minimum, use ``idxmin``. This is "
            "the equivalent of the ``numpy.ndarray`` method ``argmin``.",
            name1=name1,
            name2=name2,
            axis_descr=axis_descr,
            min_count="",
            see_also=_stat_func_see_also,
            examples=_min_examples,
        )
        def min(
            self,
            axis: int | None | lib.NoDefault = lib.no_default,
            skipna=True,
            level=None,
            numeric_only=None,
            **kwargs,
        ):
            return NDFrame.min(self, axis, skipna, level, numeric_only, **kwargs)

        setattr(cls, "min", min)
