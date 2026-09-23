    @classmethod
    def from_exception(cls, exc):
        return cls(type(exc), *exc.args)
