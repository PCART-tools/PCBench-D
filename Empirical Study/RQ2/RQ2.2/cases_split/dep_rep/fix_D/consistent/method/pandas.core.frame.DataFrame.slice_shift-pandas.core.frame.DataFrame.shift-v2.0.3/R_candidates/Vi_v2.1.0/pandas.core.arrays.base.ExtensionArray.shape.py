    @property
    def shape(self) -> Shape:
        """
        Return a tuple of the array dimensions.

        Examples
        --------
        >>> arr = pd.array([1, 2, 3])
        >>> arr.shape
        (3,)
        """
        return (len(self),)
