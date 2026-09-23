    @property
    def minposx(self):
        """
        The minimum positive value in the *x*-direction within the Bbox.

        This is useful when dealing with logarithmic scales and other scales
        where negative bounds result in floating point errors, and will be used
        as the minimum *x*-extent instead of *x0*.
        """
        return self._minpos[0]
