    def __deepcopy__(self: FrameOrSeries, memo=None) -> FrameOrSeries:
        """
        Parameters
        ----------
        memo, default None
            Standard signature. Unused
        """
        return self.copy(deep=True)
