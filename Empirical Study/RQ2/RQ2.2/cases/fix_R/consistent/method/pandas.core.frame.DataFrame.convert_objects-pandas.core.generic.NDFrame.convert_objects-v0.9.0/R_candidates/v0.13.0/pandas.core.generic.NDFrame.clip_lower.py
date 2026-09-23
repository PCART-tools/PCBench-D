    def clip_lower(self, threshold):
        """
        Return copy of the input with values below given value truncated

        See also
        --------
        clip

        Returns
        -------
        clipped : same type as input
        """
        if isnull(threshold):
            raise ValueError("Cannot use an NA value as a clip threshold")

        return self.where((self >= threshold) | isnull(self), threshold)
