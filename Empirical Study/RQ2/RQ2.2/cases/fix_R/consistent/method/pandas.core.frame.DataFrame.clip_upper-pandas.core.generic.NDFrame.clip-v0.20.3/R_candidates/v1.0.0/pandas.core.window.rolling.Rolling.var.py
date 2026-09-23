    @Substitution(name="rolling", versionadded="")
    @Appender(_shared_docs["var"])
    def var(self, ddof=1, *args, **kwargs):
        nv.validate_rolling_func("var", args, kwargs)
        return super().var(ddof=ddof, **kwargs)
