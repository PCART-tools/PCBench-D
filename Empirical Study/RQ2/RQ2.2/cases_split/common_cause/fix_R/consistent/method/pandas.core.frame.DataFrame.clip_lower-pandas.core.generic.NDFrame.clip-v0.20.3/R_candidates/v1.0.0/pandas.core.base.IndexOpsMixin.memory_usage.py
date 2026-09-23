    def memory_usage(self, deep=False):
        """
        Memory usage of the values.

        Parameters
        ----------
        deep : bool
            Introspect the data deeply, interrogate
            `object` dtypes for system-level memory consumption.

        Returns
        -------
        bytes used

        See Also
        --------
        numpy.ndarray.nbytes

        Notes
        -----
        Memory usage does not include memory consumed by elements that
        are not components of the array if deep=False or if used on PyPy
        """
        if hasattr(self.array, "memory_usage"):
            return self.array.memory_usage(deep=deep)

        v = self.array.nbytes
        if deep and is_object_dtype(self) and not PYPY:
            v += lib.memory_usage_of_objects(self.array)
        return v
