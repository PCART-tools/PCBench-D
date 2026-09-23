def _csc_gen_triples(A):
    """Converts a SciPy sparse array in **Compressed Sparse Column** format to
    an iterable of weighted edge triples.

    """
    ncols = A.shape[1]
    data, indices, indptr = A.data, A.indices, A.indptr
    for i in range(ncols):
        for j in range(indptr[i], indptr[i + 1]):
            yield indices[j], i, data[j]
