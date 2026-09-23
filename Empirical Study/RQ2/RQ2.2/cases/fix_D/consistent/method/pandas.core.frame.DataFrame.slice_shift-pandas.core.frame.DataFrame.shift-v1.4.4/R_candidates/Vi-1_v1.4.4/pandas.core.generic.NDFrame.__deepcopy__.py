    @final
    def __deepcopy__(self: NDFrameT, memo=None) -> NDFrameT:
        """
        Parameters
        ----------
        memo, default None
            Standard signature. Unused
        """
        return self.copy(deep=True)
