    def _memory_usage(self, deep: bool = False) -> int:
        """
        Memory usage of the values.

        Parameters
        ----------
        deep : bool, default False
            Introspect the data deeply, interrogate
            `object` dtypes for system-level memory consumption.

        Returns
        -------
        bytes used

        See Also
        --------
        numpy.ndarray.nbytes : Total bytes consumed by the elements of the
            array.

        Notes
        -----
        Memory usage does not include memory consumed by elements that
        are not components of the array if deep=False or if used on PyPy
        """
        if hasattr(self.array, "memory_usage"):
            # https://github.com/python/mypy/issues/1424
            # error: "ExtensionArray" has no attribute "memory_usage"
            return self.array.memory_usage(deep=deep)  # type: ignore[attr-defined]

        v = self.array.nbytes
        if deep and is_object_dtype(self) and not PYPY:
            values = cast(np.ndarray, self._values)
            v += lib.memory_usage_of_objects(values)
        return v
