    def view(self, dtype, order='C'):
        """ Get a view of the array as a new data type

        Parameters
        ----------
        dtype:
            The dtype by which to view the array
        order: string
            'C' or 'F' (Fortran) ordering

        This reinterprets the bytes of the array under a new dtype.  If that
        dtype does not have the same size as the original array then the shape
        will change.

        Beware that both numpy and dask.array can behave oddly when taking
        shape-changing views of arrays under Fortran ordering.  Under some
        versions of NumPy this function will fail when taking shape-changing
        views of Fortran ordered arrays if the first dimension has chunks of
        size one.
        """
        dtype = np.dtype(dtype)
        mult = self.dtype.itemsize / dtype.itemsize

        if order == 'C':
            ascontiguousarray = np.ascontiguousarray
            chunks = self.chunks[:-1] + (tuple(ensure_int(c * mult)
                                         for c in self.chunks[-1]),)
        elif order == 'F':
            ascontiguousarray = np.asfortranarray
            chunks = ((tuple(ensure_int(c * mult) for c in self.chunks[0]), ) +
                      self.chunks[1:])
        else:
            raise ValueError("Order must be one of 'C' or 'F'")

        out = elemwise(ascontiguousarray, self, dtype=self.dtype)
        out = elemwise(np.ndarray.view, out, dtype, dtype=dtype)
        out._chunks = chunks
        return out
