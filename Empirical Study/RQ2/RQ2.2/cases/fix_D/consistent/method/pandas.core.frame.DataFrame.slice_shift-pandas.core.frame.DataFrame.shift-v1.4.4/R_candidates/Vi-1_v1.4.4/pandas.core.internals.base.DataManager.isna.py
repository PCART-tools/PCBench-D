    @final
    def isna(self: T, func) -> T:
        return self.apply("apply", func=func)
