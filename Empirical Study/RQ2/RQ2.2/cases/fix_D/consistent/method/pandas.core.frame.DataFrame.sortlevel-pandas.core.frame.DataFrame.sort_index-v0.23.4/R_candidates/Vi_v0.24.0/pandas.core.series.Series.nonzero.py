    def nonzero(self):
        """
        Return the *integer* indices of the elements that are non-zero.

        .. deprecated:: 0.24.0
           Please use .to_numpy().nonzero() as a replacement.

        This method is equivalent to calling `numpy.nonzero` on the
        series data. For compatibility with NumPy, the return value is
        the same (a tuple with an array of indices for each dimension),
        but it will always be a one-item tuple because series only have
        one dimension.

        See Also
        --------
        numpy.nonzero

        Examples
        --------
        >>> s = pd.Series([0, 3, 0, 4])
        >>> s.nonzero()
        (array([1, 3]),)
        >>> s.iloc[s.nonzero()[0]]
        1    3
        3    4
        dtype: int64

        >>> s = pd.Series([0, 3, 0, 4], index=['a', 'b', 'c', 'd'])
        # same return although index of s is different
        >>> s.nonzero()
        (array([1, 3]),)
        >>> s.iloc[s.nonzero()[0]]
        b    3
        d    4
        dtype: int64
        """
        msg = ("Series.nonzero() is deprecated "
               "and will be removed in a future version."
               "Use Series.to_numpy().nonzero() instead")
        warnings.warn(msg, FutureWarning, stacklevel=2)
        return self._values.nonzero()
