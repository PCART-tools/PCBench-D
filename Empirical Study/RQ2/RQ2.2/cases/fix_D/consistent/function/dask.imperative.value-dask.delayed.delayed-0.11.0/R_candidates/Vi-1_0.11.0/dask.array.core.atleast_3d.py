def atleast_3d(x):
    if x.ndim == 1:
        return x[None, :, None]
    elif x.ndim == 2:
        return x[:, :, None]
    elif x.ndim > 2:
        return x
    else:
        raise NotImplementedError()
