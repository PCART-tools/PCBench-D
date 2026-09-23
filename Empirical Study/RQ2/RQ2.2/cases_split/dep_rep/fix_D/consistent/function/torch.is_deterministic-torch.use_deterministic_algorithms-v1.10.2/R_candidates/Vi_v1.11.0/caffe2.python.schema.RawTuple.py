def RawTuple(num_fields, name_prefix='field'):
    """
    Creates a tuple of `num_field` untyped scalars.
    """
    assert isinstance(num_fields, int)
    assert num_fields >= 0
    return NamedTuple(name_prefix, *([np.void] * num_fields))
