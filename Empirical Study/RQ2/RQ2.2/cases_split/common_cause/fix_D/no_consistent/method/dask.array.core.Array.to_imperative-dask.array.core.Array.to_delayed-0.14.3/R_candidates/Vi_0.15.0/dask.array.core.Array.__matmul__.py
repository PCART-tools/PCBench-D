    def __matmul__(self, other):
        if not hasattr(other, 'ndim'):
            other = np.asarray(other)  # account for array-like RHS
        if other.ndim > 2:
            msg = ('The matrix multiplication operator (@) is not yet '
                   'implemented for higher-dimensional Dask arrays. Try '
                   '`dask.array.tensordot` and see the discussion at '
                   'https://github.com/dask/dask/pull/2349 for details.')
            raise NotImplementedError(msg)
        return tensordot(self, other, axes=((self.ndim - 1,),
                                            (other.ndim - 2,)))
