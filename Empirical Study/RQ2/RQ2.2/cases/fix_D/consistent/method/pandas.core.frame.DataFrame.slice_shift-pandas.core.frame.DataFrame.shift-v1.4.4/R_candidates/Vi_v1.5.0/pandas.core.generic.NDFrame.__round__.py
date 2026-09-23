    @final
    def __round__(self: NDFrameT, decimals: int = 0) -> NDFrameT:
        return self.round(decimals).__finalize__(self, method="__round__")
