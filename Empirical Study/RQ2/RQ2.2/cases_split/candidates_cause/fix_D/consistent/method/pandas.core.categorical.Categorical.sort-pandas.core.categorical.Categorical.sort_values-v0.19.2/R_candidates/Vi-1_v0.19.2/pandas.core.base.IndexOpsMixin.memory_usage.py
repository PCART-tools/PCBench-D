    def memory_usage(self, deep=False):
        """
        Memory usage of my values

        Parameters
        ----------
        deep : bool
            Introspect the data deeply, interrogate
            `object` dtypes for system-level memory consumption

        Returns
        -------
        bytes used

        Notes
        -----
        Memory usage does not include memory consumed by elements that
        are not components of the array if deep=False

        See Also
        --------
        numpy.ndarray.nbytes
        """
        if hasattr(self.values, 'memory_usage'):
            return self.values.memory_usage(deep=deep)

        v = self.values.nbytes
        if deep and is_object_dtype(self):
            v += lib.memory_usage_of_objects(self.values)
        return v
