    @Substitution(name="rolling")
    @Appender(_shared_docs["min"])
    def min(self, *args, **kwargs):
        nv.validate_rolling_func("min", args, kwargs)
        return super().min(*args, **kwargs)
