    @Substitution(name="expanding")
    @Appender(_shared_docs["min"])
    def min(self, *args, **kwargs):
        nv.validate_expanding_func("min", args, kwargs)
        return super().min(*args, **kwargs)
