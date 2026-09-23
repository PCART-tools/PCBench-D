    @final
    def __deepcopy__(self: _IndexT, memo=None) -> _IndexT:
        """
        Parameters
        ----------
        memo, default None
            Standard signature. Unused
        """
        return self.copy(deep=True)
