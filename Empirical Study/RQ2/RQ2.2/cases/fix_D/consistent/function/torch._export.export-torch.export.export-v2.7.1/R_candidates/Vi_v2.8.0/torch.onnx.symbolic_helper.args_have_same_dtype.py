def args_have_same_dtype(args):
    assert args
    base_dtype = _type_utils.JitScalarType.from_value(args[0])
    has_same_dtype = all(
        _type_utils.JitScalarType.from_value(elem) == base_dtype for elem in args
    )
    return has_same_dtype
