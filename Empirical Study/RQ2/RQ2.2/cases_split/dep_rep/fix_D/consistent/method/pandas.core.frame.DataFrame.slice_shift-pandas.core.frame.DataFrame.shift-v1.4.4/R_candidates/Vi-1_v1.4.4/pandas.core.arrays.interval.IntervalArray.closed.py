    @property
    def closed(self):
        """
        Whether the intervals are closed on the left-side, right-side, both or
        neither.
        """
        return self.dtype.closed
