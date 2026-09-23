    @Substitution(name="ewm")
    @Appender(_doc_template)
    @Appender(_bias_template)
    def std(self, bias=False, *args, **kwargs):
        """
        Exponential weighted moving stddev.
        """
        nv.validate_window_func("std", args, kwargs)
        return zsqrt(self.var(bias=bias, **kwargs))
