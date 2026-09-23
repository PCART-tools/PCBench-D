    def get_xbound(self):
        """Returns the x-axis numerical bounds

        This always returns::

          lowerBound < upperBound

        Returns
        -------
        lowerBound, upperBound : float

        """
        left, right = self.get_xlim()
        if left < right:
            return left, right
        else:
            return right, left
