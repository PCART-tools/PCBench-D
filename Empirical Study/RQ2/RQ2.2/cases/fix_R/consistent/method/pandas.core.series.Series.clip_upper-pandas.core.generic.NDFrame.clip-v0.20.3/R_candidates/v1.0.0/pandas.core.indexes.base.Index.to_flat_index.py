    def to_flat_index(self):
        """
        Identity method.

        .. versionadded:: 0.24.0

        This is implemented for compatibility with subclass implementations
        when chaining.

        Returns
        -------
        pd.Index
            Caller.

        See Also
        --------
        MultiIndex.to_flat_index : Subclass implementation.
        """
        return self
