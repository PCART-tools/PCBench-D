def maybe_clone(x):
    if x is not None:
        return clone_preserve_strides(x)
    return x
