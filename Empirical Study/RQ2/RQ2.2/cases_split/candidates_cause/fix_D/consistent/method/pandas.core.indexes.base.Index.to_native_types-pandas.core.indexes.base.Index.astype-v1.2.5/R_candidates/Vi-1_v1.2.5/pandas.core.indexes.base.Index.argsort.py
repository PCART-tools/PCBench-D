    def argsort(self, *args, **kwargs) -> np.ndarray:
        """
        Return the integer indices that would sort the index.

        Parameters
        ----------
        *args
            Passed to `numpy.ndarray.argsort`.
        **kwargs
            Passed to `numpy.ndarray.argsort`.

        Returns
        -------
        numpy.ndarray
            Integer indices that would sort the index if used as
            an indexer.

        See Also
        --------
        numpy.argsort : Similar method for NumPy arrays.
        Index.sort_values : Return sorted copy of Index.

        Examples
        --------
        >>> idx = pd.Index(['b', 'a', 'd', 'c'])
        >>> idx
        Index(['b', 'a', 'd', 'c'], dtype='object')

        >>> order = idx.argsort()
        >>> order
        array([1, 0, 3, 2])

        >>> idx[order]
        Index(['a', 'b', 'c', 'd'], dtype='object')
        """
        if needs_i8_conversion(self.dtype):
            # TODO: these do not match the underlying EA argsort methods GH#37863
            return self.asi8.argsort(*args, **kwargs)

        # This works for either ndarray or EA, is overriden
        #  by RangeIndex, MultIIndex
        return self._data.argsort(*args, **kwargs)
