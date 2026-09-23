    @Substitution(name="expanding")
    @Appender(_shared_docs["std"])
    def std(self, ddof=1, *args, **kwargs):
        nv.validate_expanding_func("std", args, kwargs)
        return super().std(ddof=ddof, **kwargs)
