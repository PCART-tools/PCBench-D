    @Substitution(name="expanding")
    @Appender(_doc_template)
    @Appender(_shared_docs["max"])
    def max(self, *args, **kwargs):
        nv.validate_expanding_func("max", args, kwargs)
        return super().max(*args, **kwargs)
