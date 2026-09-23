    @property
    def ndim(self) -> int:
        """
        Extension Arrays are only allowed to be 1-dimensional.

        Examples
        --------
        >>> arr = pd.array([1, 2, 3])
        >>> arr.ndim
        1
        """
        return 1
