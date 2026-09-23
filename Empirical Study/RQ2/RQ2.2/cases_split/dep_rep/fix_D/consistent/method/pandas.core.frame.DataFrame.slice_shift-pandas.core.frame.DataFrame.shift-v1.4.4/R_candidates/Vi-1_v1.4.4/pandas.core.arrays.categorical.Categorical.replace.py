    def replace(self, to_replace, value, inplace: bool = False):
        """
        Replaces all instances of one value with another

        Parameters
        ----------
        to_replace: object
            The value to be replaced

        value: object
            The value to replace it with

        inplace: bool
            Whether the operation is done in-place

        Returns
        -------
        None if inplace is True, otherwise the new Categorical after replacement


        Examples
        --------
        >>> s = pd.Categorical([1, 2, 1, 3])
        >>> s.replace(1, 3)
        [3, 2, 3, 3]
        Categories (2, int64): [2, 3]
        """
        # GH#44929 deprecation
        warn(
            "Categorical.replace is deprecated and will be removed in a future "
            "version. Use Series.replace directly instead.",
            FutureWarning,
            stacklevel=find_stack_level(),
        )
        return self._replace(to_replace=to_replace, value=value, inplace=inplace)
