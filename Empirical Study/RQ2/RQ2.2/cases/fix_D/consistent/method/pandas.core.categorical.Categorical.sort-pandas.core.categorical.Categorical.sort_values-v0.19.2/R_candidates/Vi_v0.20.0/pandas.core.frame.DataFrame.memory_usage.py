    def memory_usage(self, index=True, deep=False):
        """Memory usage of DataFrame columns.

        Parameters
        ----------
        index : bool
            Specifies whether to include memory usage of DataFrame's
            index in returned Series. If `index=True` (default is False)
            the first index of the Series is `Index`.
        deep : bool
            Introspect the data deeply, interrogate
            `object` dtypes for system-level memory consumption

        Returns
        -------
        sizes : Series
            A series with column names as index and memory usage of
            columns with units of bytes.

        Notes
        -----
        Memory usage does not include memory consumed by elements that
        are not components of the array if deep=False

        See Also
        --------
        numpy.ndarray.nbytes
        """
        result = Series([c.memory_usage(index=False, deep=deep)
                         for col, c in self.iteritems()], index=self.columns)
        if index:
            result = Series(self.index.memory_usage(deep=deep),
                            index=['Index']).append(result)
        return result
