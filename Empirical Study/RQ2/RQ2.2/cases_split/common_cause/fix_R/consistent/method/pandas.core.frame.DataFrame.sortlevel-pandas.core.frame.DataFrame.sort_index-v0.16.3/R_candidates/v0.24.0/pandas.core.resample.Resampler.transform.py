    def transform(self, arg, *args, **kwargs):
        """
        Call function producing a like-indexed Series on each group and return
        a Series with the transformed values.

        Parameters
        ----------
        func : function
            To apply to each group. Should return a Series with the same index

        Returns
        -------
        transformed : Series

        Examples
        --------
        >>> resampled.transform(lambda x: (x - x.mean()) / x.std())
        """
        return self._selected_obj.groupby(self.groupby).transform(
            arg, *args, **kwargs)
