def atleast_2d(x):
    if x.ndim == 1:
        return x[None, :]
    elif x.ndim > 1:
        return x
    else:
        raise NotImplementedError()
