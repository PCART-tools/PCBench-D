    @property
    def nbytes(self) -> int:
        """
        The number of bytes needed to store this object in memory.

        Examples
        --------
        >>> pd.array([1, 2, 3]).nbytes
        27
        """
        # If this is expensive to compute, return an approximate lower bound
        # on the number of bytes needed.
        raise AbstractMethodError(self)
