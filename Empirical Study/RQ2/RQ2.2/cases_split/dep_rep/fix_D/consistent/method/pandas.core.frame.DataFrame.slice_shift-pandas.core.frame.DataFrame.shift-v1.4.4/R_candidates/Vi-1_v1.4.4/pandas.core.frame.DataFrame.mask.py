    @deprecate_nonkeyword_arguments(
        version=None, allowed_args=["self", "cond", "other"]
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
        return super().mask(cond, other, inplace, axis, level, errors, try_cast)
