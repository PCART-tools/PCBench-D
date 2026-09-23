    @deprecate_nonkeyword_arguments(
        version=None, allowed_args=["self", "cond", "other"]
    )
    def where(
        self,
        cond,
        other=lib.no_default,
        inplace=False,
        axis=None,
        level=None,
        errors="raise",
        try_cast=lib.no_default,
    ):
        return super().where(cond, other, inplace, axis, level, errors, try_cast)
