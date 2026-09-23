    def clip_upper(self, threshold, axis=None, inplace=False):
        """
        Return copy of input with values above given value(s) truncated.

        Parameters
        ----------
        threshold : float or array_like
        axis : int or string axis name, optional
            Align object with threshold along the given axis.
        inplace : boolean, default False
            Whether to perform the operation in place on the data
                .. versionadded:: 0.21.0

        See Also
        --------
        clip

        Returns
        -------
        clipped : same type as input
        """
        return self._clip_with_one_bound(threshold, method=self.le,
                                         axis=axis, inplace=inplace)
