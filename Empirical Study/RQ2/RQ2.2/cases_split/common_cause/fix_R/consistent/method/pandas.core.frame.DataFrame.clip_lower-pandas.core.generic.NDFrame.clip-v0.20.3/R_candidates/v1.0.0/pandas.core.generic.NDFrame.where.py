    @Appender(
        _shared_docs["where"]
        % dict(
            _shared_doc_kwargs,
            cond="True",
            cond_rev="False",
            name="where",
            name_other="mask",
        )
    )
    def where(
        self,
        cond,
        other=np.nan,
        inplace=False,
        axis=None,
        level=None,
        errors="raise",
        try_cast=False,
    ):

        other = com.apply_if_callable(other, self)
        return self._where(
            cond, other, inplace, axis, level, errors=errors, try_cast=try_cast
        )
