    def to_numpy(self) -> np.ndarray[Any, Any]:
        """
        Convert DataFrame to a 2D NumPy array.

        This operation clones data.

        Notes
        -----
        If you're attempting to convert Utf8 to an array you'll need to install
        ``pyarrow``.

        Examples
        --------
        >>> df = pl.DataFrame(
        ...     {"foo": [1, 2, 3], "bar": [6, 7, 8], "ham": ["a", "b", "c"]}
        ... )
        >>> numpy_array = df.to_numpy()
        >>> type(numpy_array)
        <class 'numpy.ndarray'>

        """
        out = self._df.to_numpy()
        if out is None:
            return np.vstack(
                [self.to_series(i).to_numpy() for i in range(self.width)]
            ).T
        else:
            return out
