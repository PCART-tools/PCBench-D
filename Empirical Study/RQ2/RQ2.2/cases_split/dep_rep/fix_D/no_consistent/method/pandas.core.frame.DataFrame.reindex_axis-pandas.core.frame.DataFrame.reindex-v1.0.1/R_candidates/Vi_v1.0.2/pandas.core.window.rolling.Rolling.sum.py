    @Substitution(name="rolling")
    @Appender(_shared_docs["sum"])
    def sum(self, *args, **kwargs):
        nv.validate_rolling_func("sum", args, kwargs)
        return super().sum(*args, **kwargs)
