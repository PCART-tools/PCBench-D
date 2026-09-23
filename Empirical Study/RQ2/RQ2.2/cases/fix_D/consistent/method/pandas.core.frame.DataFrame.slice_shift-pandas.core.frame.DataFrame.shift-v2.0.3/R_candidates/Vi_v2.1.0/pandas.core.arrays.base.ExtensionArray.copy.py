    def copy(self) -> Self:
        """
        Return a copy of the array.

        Returns
        -------
        ExtensionArray

        Examples
        --------
        >>> arr = pd.array([1, 2, 3])
        >>> arr2 = arr.copy()
        >>> arr[0] = 2
        >>> arr2
        <IntegerArray>
        [1, 2, 3]
        Length: 3, dtype: Int64
        """
        raise AbstractMethodError(self)
