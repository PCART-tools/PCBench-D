    @Substitution(name="window", versionadded="\n.. versionadded:: 1.0.0\n")
    @Appender(_shared_docs["std"])
    def std(self, ddof=1, *args, **kwargs):
        nv.validate_window_func("std", args, kwargs)
        return zsqrt(self.var(ddof=ddof, name="std", **kwargs))
