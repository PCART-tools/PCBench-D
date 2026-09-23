    def __init__(self, minor=False, *, nbins="auto"):
        """
        Parameters
        ----------
        nbins : int or 'auto', optional
            Number of ticks. Only used if minor is False.
        minor : bool, default: False
            Indicate if this locator is for minor ticks or not.
        """

        self._minor = minor
        super().__init__(nbins=nbins, steps=[1, 2, 5, 10])
