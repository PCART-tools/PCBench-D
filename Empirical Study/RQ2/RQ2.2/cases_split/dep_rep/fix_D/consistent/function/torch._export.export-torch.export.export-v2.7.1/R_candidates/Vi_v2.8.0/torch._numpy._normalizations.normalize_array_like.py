def normalize_array_like(x, parm=None):
    from ._ndarray import asarray

    return asarray(x).tensor
