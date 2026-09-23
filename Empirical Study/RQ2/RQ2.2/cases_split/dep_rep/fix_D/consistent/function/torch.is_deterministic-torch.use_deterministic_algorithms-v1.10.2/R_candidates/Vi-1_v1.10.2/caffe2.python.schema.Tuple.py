def Tuple(*fields):
    """
    Creates a Struct with default, sequential, field names of given types.
    """
    return NamedTuple('field', *fields)
