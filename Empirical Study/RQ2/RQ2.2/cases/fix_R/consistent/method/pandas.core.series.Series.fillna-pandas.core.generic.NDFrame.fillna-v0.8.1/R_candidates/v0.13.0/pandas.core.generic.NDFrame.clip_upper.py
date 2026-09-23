    def clip_upper(self, threshold):
        """
        Return copy of input with values above given value truncated

        See also
        --------
        clip

        Returns
        -------
        clipped : same type as input
        """
        if isnull(threshold):
            raise ValueError("Cannot use an NA value as a clip threshold")

        return self.where((self <= threshold) | isnull(self), threshold)
