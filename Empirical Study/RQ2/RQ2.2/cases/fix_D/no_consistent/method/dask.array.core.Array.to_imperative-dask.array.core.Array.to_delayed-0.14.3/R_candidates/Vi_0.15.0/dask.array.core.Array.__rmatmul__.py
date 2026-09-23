    def __rmatmul__(self, other):
        if not hasattr(other, 'ndim'):
            other = np.asarray(other)  # account for array-like on LHS
        if self.ndim > 2:
            msg = ('The matrix multiplication operator (@) is not yet '
                   'implemented for higher-dimensional Dask arrays. Try '
                   '`dask.array.tensordot` and see the discussion at '
                   'https://github.com/dask/dask/pull/2349 for details.')
            raise NotImplementedError(msg)
        return tensordot(other, self, axes=((other.ndim - 1,),
                                            (self.ndim - 2,)))
