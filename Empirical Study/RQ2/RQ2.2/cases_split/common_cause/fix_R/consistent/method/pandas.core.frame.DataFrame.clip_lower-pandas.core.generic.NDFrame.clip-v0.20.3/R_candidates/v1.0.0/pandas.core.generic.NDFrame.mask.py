    @Appender(
        _shared_docs["where"]
        % dict(
            _shared_doc_kwargs,
            cond="False",
            cond_rev="True",
            name="mask",
            name_other="where",
        )
    )
    def mask(
        self,
        cond,
        other=np.nan,
        inplace=False,
        axis=None,
        level=None,
        errors="raise",
        try_cast=False,
    ):

        inplace = validate_bool_kwarg(inplace, "inplace")
        cond = com.apply_if_callable(cond, self)

        # see gh-21891
        if not hasattr(cond, "__invert__"):
            cond = np.array(cond)

        return self.where(
            ~cond,
            other=other,
            inplace=inplace,
            axis=axis,
            level=level,
            try_cast=try_cast,
            errors=errors,
        )
