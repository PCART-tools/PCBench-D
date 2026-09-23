    @property
    def size(self) -> int:
        """
        Return an int representing the number of elements in this object.

        Return the number of rows if Series. Otherwise return the number of
        rows times number of columns if DataFrame.

        See Also
        --------
        ndarray.size : Number of elements in the array.

        Examples
        --------
        >>> s = pd.Series({'a': 1, 'b': 2, 'c': 3})
        >>> s.size
        3

        >>> df = pd.DataFrame({'col1': [1, 2], 'col2': [3, 4]})
        >>> df.size
        4
        """
        # error: Incompatible return value type (got "signedinteger[_64Bit]",
        # expected "int")  [return-value]
        return np.prod(self.shape)  # type: ignore[return-value]
