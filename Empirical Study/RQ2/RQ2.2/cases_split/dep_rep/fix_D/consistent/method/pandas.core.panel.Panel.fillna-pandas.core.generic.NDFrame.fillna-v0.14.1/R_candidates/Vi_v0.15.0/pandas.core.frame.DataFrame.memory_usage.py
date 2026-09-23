    def memory_usage(self, index=False):
        """Memory usage of DataFrame columns.

        Parameters
        ----------
        index : bool
            Specifies whether to include memory usage of DataFrame's
            index in returned Series. If `index=True` (default is False)
            the first index of the Series is `Index`.

        Returns
        -------
        sizes : Series
            A series with column names as index and memory usage of
            columns with units of bytes.

        Notes
        -----
        Memory usage does not include memory consumed by elements that
        are not components of the array.

        See Also
        --------
        numpy.ndarray.nbytes
        """
        result = Series([ c.values.nbytes for col, c in self.iteritems() ],
                        index=self.columns)
        if index:
             result = Series(self.index.values.nbytes,
                        index=['Index']).append(result)
        return result
