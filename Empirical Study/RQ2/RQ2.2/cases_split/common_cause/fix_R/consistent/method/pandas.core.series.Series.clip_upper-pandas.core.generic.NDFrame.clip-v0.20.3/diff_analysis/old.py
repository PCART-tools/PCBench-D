    def clip_upper(self, threshold, axis=None):
        """
        Return copy of input with values above given value(s) truncated.

        Parameters
        ----------
        threshold : float or array_like
        axis : int or string axis name, optional
            Align object with threshold along the given axis.

        See Also
        --------
        clip

        Returns
        -------
        clipped : same type as input
        """
        if np.any(isnull(threshold)):
            raise ValueError("Cannot use an NA value as a clip threshold")

        if is_scalar(threshold) and is_number(threshold):
            return self._clip_with_scalar(None, threshold)

        subset = self.le(threshold, axis=axis) | isnull(self)
        return self.where(subset, threshold, axis=axis)
