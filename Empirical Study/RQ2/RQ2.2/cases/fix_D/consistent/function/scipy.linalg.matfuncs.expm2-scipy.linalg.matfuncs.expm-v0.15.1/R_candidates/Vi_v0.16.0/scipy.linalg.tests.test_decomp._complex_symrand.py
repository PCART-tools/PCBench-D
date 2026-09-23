def _complex_symrand(dim, dtype):
    a1, a2 = symrand(dim), symrand(dim)
    # add antisymmetric matrix as imag part
    a = a1 + 1j*(triu(a2)-tril(a2))
    return a.astype(dtype)
