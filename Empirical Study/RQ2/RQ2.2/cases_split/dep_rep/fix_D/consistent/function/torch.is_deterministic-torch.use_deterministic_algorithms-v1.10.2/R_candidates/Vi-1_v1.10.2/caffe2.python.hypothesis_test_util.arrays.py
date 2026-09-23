def arrays(dims, dtype=np.float32, elements=None, unique=False):
    if elements is None:
        elements = elements_of_type(dtype)
    return hypothesis.extra.numpy.arrays(
        dtype,
        dims,
        elements=elements,
        unique=unique,
    )
