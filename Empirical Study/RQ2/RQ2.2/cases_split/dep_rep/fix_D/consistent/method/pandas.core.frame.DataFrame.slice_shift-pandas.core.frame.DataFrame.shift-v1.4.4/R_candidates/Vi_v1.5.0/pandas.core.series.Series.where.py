    @deprecate_kwarg(old_arg_name="errors", new_arg_name=None)
    @deprecate_nonkeyword_arguments(
        version=None, allowed_args=["self", "cond", "other"]
    )
    def where(  # type: ignore[override]
        self,
        cond,
        other=lib.no_default,
        inplace: bool = False,
        axis: Axis | None = None,
        level: Level = None,
        errors: IgnoreRaise | lib.NoDefault = lib.no_default,
        try_cast: bool | lib.NoDefault = lib.no_default,
    ) -> Series | None:
        return super().where(
            cond,
            other,
            inplace=inplace,
            axis=axis,
            level=level,
            try_cast=try_cast,
        )
