    def nonzero(self):
        """
        Return the indices of the elements that are non-zero

        This method is equivalent to calling `numpy.nonzero` on the
        series data. For compatability with NumPy, the return value is
        the same (a tuple with an array of indices for each dimension),
        but it will always be a one-item tuple because series only have
        one dimension.

        Examples
        --------
        >>> s = pd.Series([0, 3, 0, 4])
        >>> s.nonzero()
        (array([1, 3]),)
        >>> s.iloc[s.nonzero()[0]]
        1    3
        3    4
        dtype: int64

        See Also
        --------
        numpy.nonzero
        """
        return self.values.nonzero()
