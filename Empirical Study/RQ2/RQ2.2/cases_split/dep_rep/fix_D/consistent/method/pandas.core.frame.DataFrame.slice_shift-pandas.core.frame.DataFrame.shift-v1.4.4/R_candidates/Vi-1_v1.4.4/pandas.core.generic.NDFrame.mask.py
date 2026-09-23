    @doc(
        where,
        klass=_shared_doc_kwargs["klass"],
        cond="False",
        cond_rev="True",
        name="mask",
        name_other="where",
    )
    def mask(
        self,
        cond,
        other=np.nan,
        inplace=False,
        axis=None,
        level=None,
        errors="raise",
        try_cast=lib.no_default,
    ):

        inplace = validate_bool_kwarg(inplace, "inplace")
        cond = com.apply_if_callable(cond, self)

        if try_cast is not lib.no_default:
            warnings.warn(
                "try_cast keyword is deprecated and will be removed in a "
                "future version.",
                FutureWarning,
                stacklevel=find_stack_level(),
            )

        # see gh-21891
        if not hasattr(cond, "__invert__"):
            cond = np.array(cond)

        return self.where(
            ~cond,
            other=other,
            inplace=inplace,
            axis=axis,
            level=level,
            errors=errors,
        )
