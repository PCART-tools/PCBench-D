    @Substitution(name="expanding")
    @Appender(_shared_docs["sum"])
    def sum(self, *args, **kwargs):
        nv.validate_expanding_func("sum", args, kwargs)
        return super().sum(*args, **kwargs)
