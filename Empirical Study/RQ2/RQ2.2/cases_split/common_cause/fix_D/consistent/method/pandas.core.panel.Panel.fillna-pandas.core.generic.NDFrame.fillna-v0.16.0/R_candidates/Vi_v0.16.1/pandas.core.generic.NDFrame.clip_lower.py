    def clip_lower(self, threshold, axis=None):
        """
        Return copy of the input with values below given value(s) truncated

        Parameters
        ----------
        threshold : float or array_like
        axis : int or string axis name, optional
            Align object with threshold along the given axis.

        See also
        --------
        clip

        Returns
        -------
        clipped : same type as input
        """
        if np.any(isnull(threshold)):
            raise ValueError("Cannot use an NA value as a clip threshold")

        subset = self.ge(threshold, axis=axis) | isnull(self)
        return self.where(subset, threshold, axis=axis)
