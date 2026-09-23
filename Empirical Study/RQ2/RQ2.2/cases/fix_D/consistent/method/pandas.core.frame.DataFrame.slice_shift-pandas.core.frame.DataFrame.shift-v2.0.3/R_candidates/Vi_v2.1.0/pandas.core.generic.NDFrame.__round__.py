    @final
    def __round__(self, decimals: int = 0) -> Self:
        return self.round(decimals).__finalize__(self, method="__round__")
