@concatenate_lookup.register_lazy('scipy')
def register_scipy_sparse():
    import scipy.sparse

    def _concatenate(L, axis=0):
        if axis == 0:
            return scipy.sparse.vstack(L)
        elif axis == 1:
            return scipy.sparse.hstack(L)
        else:
            msg = ("Can only concatenate scipy sparse matrices for axis in "
                   "{0, 1}.  Got %s" % axis)
            raise ValueError(msg)
    concatenate_lookup.register(scipy.sparse.spmatrix, _concatenate)
