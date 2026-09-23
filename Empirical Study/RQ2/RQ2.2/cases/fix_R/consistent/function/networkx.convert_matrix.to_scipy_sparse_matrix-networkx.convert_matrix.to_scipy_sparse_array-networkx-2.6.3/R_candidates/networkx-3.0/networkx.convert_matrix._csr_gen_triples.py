def _csr_gen_triples(A):
    """Converts a SciPy sparse array in **Compressed Sparse Row** format to
    an iterable of weighted edge triples.

    """
    nrows = A.shape[0]
    data, indices, indptr = A.data, A.indices, A.indptr
    for i in range(nrows):
        for j in range(indptr[i], indptr[i + 1]):
            yield i, indices[j], data[j]
