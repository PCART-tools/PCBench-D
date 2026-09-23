    def memory_usage(self, index=True, deep=False):
        """Memory usage of the Series

        Parameters
        ----------
        index : bool
            Specifies whether to include memory usage of Series index
        deep : bool
            Introspect the data deeply, interrogate
            `object` dtypes for system-level memory consumption

        Returns
        -------
        scalar bytes of memory consumed

        Notes
        -----
        Memory usage does not include memory consumed by elements that
        are not components of the array if deep=False

        See Also
        --------
        numpy.ndarray.nbytes
        """
        v = super(Series, self).memory_usage(deep=deep)
        if index:
            v += self.index.memory_usage(deep=deep)
        return v
