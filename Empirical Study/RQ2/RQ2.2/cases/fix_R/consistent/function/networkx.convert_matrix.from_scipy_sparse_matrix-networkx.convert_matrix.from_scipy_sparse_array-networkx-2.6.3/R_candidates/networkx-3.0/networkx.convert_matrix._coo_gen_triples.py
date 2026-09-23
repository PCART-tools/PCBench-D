def _coo_gen_triples(A):
    """Converts a SciPy sparse array in **Coordinate** format to an iterable
    of weighted edge triples.

    """
    row, col, data = A.row, A.col, A.data
    return zip(row, col, data)
