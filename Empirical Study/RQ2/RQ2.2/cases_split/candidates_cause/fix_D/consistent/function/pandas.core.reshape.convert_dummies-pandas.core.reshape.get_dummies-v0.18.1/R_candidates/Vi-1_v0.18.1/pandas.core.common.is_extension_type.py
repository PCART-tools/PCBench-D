def is_extension_type(value):
    """
    if we are a klass that is preserved by the internals
    these are internal klasses that we represent (and don't use a np.array)
    """
    if is_categorical(value):
        return True
    elif is_sparse(value):
        return True
    elif is_datetimetz(value):
        return True
    return False
