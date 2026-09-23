    @property
    def values(self) -> ArrayLike:
        """
        Return an array representing the data in the Index.

        .. warning::

           We recommend using :attr:`Index.array` or
           :meth:`Index.to_numpy`, depending on whether you need
           a reference to the underlying data or a NumPy array.

        Returns
        -------
        array: numpy.ndarray or ExtensionArray

        See Also
        --------
        Index.array : Reference to the underlying data.
        Index.to_numpy : A NumPy array representing the underlying data.

        Examples
        --------
        For :class:`pandas.Index`:

        >>> idx = pd.Index([1, 2, 3])
        >>> idx
        Index([1, 2, 3], dtype='int64')
        >>> idx.values
        array([1, 2, 3])

        For :class:`pandas.IntervalIndex`:

        >>> idx = pd.interval_range(start=0, end=5)
        >>> idx.values
        <IntervalArray>
        [(0, 1], (1, 2], (2, 3], (3, 4], (4, 5]]
        Length: 5, dtype: interval[int64, right]
        """
        if using_copy_on_write():
            data = self._data
            if isinstance(data, np.ndarray):
                data = data.view()
                data.flags.writeable = False
            return data
        return self._data
