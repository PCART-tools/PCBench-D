    @classmethod
    def _add_numeric_operations(cls) -> None:
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
        def any(
            self,
            *,
            axis: Axis = 0,
            bool_only=None,
            skipna: bool_t = True,
            **kwargs,
        ):
            return NDFrame.any(
                self,
                axis=axis,
                bool_only=bool_only,
                skipna=skipna,
                **kwargs,
            )

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
        def all(
            self,
            axis: Axis = 0,
            bool_only=None,
            skipna: bool_t = True,
            **kwargs,
        ):
            return NDFrame.all(self, axis, bool_only, skipna, **kwargs)

        setattr(cls, "all", all)

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
            axis: Axis | None = None,
            skipna: bool_t = True,
            ddof: int = 1,
            numeric_only: bool_t = False,
            **kwargs,
        ):
            return NDFrame.sem(self, axis, skipna, ddof, numeric_only, **kwargs)

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
            axis: Axis | None = None,
            skipna: bool_t = True,
            ddof: int = 1,
            numeric_only: bool_t = False,
            **kwargs,
        ):
            return NDFrame.var(self, axis, skipna, ddof, numeric_only, **kwargs)

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
            axis: Axis | None = None,
            skipna: bool_t = True,
            ddof: int = 1,
            numeric_only: bool_t = False,
            **kwargs,
        ):
            return NDFrame.std(self, axis, skipna, ddof, numeric_only, **kwargs)

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
        def cummin(
            self, axis: Axis | None = None, skipna: bool_t = True, *args, **kwargs
        ):
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
        def cummax(
            self, axis: Axis | None = None, skipna: bool_t = True, *args, **kwargs
        ):
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
        def cumsum(
            self, axis: Axis | None = None, skipna: bool_t = True, *args, **kwargs
        ):
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
        def cumprod(
            self, axis: Axis | None = None, skipna: bool_t = True, *args, **kwargs
        ):
            return NDFrame.cumprod(self, axis, skipna, *args, **kwargs)

        setattr(cls, "cumprod", cumprod)

        # error: Untyped decorator makes function "sum" untyped
        @doc(  # type: ignore[misc]
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
            axis: Axis | None = None,
            skipna: bool_t = True,
            numeric_only: bool_t = False,
            min_count: int = 0,
            **kwargs,
        ):
            return NDFrame.sum(self, axis, skipna, numeric_only, min_count, **kwargs)

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
            axis: Axis | None = None,
            skipna: bool_t = True,
            numeric_only: bool_t = False,
            min_count: int = 0,
            **kwargs,
        ):
            return NDFrame.prod(self, axis, skipna, numeric_only, min_count, **kwargs)

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
            axis: AxisInt | None = 0,
            skipna: bool_t = True,
            numeric_only: bool_t = False,
            **kwargs,
        ):
            return NDFrame.mean(self, axis, skipna, numeric_only, **kwargs)

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
            axis: AxisInt | None = 0,
            skipna: bool_t = True,
            numeric_only: bool_t = False,
            **kwargs,
        ):
            return NDFrame.skew(self, axis, skipna, numeric_only, **kwargs)

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
            axis: Axis | None = 0,
            skipna: bool_t = True,
            numeric_only: bool_t = False,
            **kwargs,
        ):
            return NDFrame.kurt(self, axis, skipna, numeric_only, **kwargs)

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
            axis: AxisInt | None = 0,
            skipna: bool_t = True,
            numeric_only: bool_t = False,
            **kwargs,
        ):
            return NDFrame.median(self, axis, skipna, numeric_only, **kwargs)

        setattr(cls, "median", median)

        @doc(
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
            axis: AxisInt | None = 0,
            skipna: bool_t = True,
            numeric_only: bool_t = False,
            **kwargs,
        ):
            return NDFrame.max(self, axis, skipna, numeric_only, **kwargs)

        setattr(cls, "max", max)

        @doc(
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
            axis: AxisInt | None = 0,
            skipna: bool_t = True,
            numeric_only: bool_t = False,
            **kwargs,
        ):
            return NDFrame.min(self, axis, skipna, numeric_only, **kwargs)

        setattr(cls, "min", min)
