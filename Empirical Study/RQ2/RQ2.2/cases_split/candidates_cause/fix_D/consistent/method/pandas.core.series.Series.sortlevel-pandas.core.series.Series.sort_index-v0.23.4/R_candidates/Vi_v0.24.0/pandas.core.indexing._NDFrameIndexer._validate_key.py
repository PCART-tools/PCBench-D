    def _validate_key(self, key, axis):
        """
        Ensure that key is valid for current indexer.

        Parameters
        ----------
        key : scalar, slice or list-like
            The key requested

        axis : int
            Dimension on which the indexing is being made

        Raises
        ------
        TypeError
            If the key (or some element of it) has wrong type

        IndexError
            If the key (or some element of it) is out of bounds

        KeyError
            If the key was not found
        """
        raise AbstractMethodError()
