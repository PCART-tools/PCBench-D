    @final
    def isna(self, func) -> Self:
        return self.apply("apply", func=func)
