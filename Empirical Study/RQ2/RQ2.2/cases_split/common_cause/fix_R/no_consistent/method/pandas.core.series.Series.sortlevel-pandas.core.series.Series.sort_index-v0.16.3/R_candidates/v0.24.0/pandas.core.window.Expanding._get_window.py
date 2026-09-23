    def _get_window(self, other=None):
        """
        Get the window length over which to perform some operation.

        Parameters
        ----------
        other : object, default None
            The other object that is involved in the operation.
            Such an object is involved for operations like covariance.

        Returns
        -------
        window : int
            The window length.
        """
        axis = self.obj._get_axis(self.axis)
        length = len(axis) + (other is not None) * len(axis)

        other = self.min_periods or -1
        return max(length, other)
