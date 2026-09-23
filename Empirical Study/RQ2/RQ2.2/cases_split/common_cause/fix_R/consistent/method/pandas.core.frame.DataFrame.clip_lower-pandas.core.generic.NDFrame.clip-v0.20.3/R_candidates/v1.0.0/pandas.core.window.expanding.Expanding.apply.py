    @Substitution(name="expanding")
    @Appender(_shared_docs["apply"])
    def apply(self, func, raw=False, args=(), kwargs={}):
        return super().apply(func, raw=raw, args=args, kwargs=kwargs)
