    @deprecate_kwarg(old_arg_name="errors", new_arg_name=None)
    @deprecate_nonkeyword_arguments(
        version=None, allowed_args=["self", "cond", "other"]
    )
    @doc(
        where,
        klass=_shared_doc_kwargs["klass"],
        cond="False",
        cond_rev="True",
        name="mask",
        name_other="where",
    )
    def mask(
        self: NDFrameT,
        cond,
        other=np.nan,
        inplace: bool_t = False,
        axis: Axis | None = None,
        level: Level = None,
        errors: IgnoreRaise | lib.NoDefault = "raise",
        try_cast: bool_t | lib.NoDefault = lib.no_default,
    ) -> NDFrameT | None:

        inplace = validate_bool_kwarg(inplace, "inplace")
        cond = com.apply_if_callable(cond, self)

        if try_cast is not lib.no_default:
            warnings.warn(
                "try_cast keyword is deprecated and will be removed in a "
                "future version.",
                FutureWarning,
                stacklevel=find_stack_level(inspect.currentframe()),
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
        )
