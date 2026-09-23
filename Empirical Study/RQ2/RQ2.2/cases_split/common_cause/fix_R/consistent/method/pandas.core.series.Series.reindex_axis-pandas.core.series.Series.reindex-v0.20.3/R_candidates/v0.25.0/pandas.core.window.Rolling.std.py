    @Substitution(name="rolling")
    @Appender(_shared_docs["std"])
    def std(self, ddof=1, *args, **kwargs):
        nv.validate_rolling_func("std", args, kwargs)
        return super().std(ddof=ddof, **kwargs)
