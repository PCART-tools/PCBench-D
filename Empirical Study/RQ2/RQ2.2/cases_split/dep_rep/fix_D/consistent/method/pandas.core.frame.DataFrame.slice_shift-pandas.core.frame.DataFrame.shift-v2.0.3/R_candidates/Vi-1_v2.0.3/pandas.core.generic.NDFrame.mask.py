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
        other=lib.no_default,
        *,
        inplace: bool_t = False,
        axis: Axis | None = None,
        level: Level = None,
    ) -> NDFrameT | None:
        inplace = validate_bool_kwarg(inplace, "inplace")
        cond = common.apply_if_callable(cond, self)

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
