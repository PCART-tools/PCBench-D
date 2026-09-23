def get_keystr(key_path: KeyPath) -> str:
    """For a given index into the flat_args, return a human readable string
    describing how to access it, e.g. "*args["foo"][0].bar"
    """
    # Prefix the keypath with "*args" or "**kwargs" to make it clearer where
    # the arguments come from. Ultimately we ought to serialize the
    # original arg names for the best error message here.
    args_kwargs_key_path = key_path[0]
    assert isinstance(args_kwargs_key_path, SequenceKey)
    if args_kwargs_key_path.idx == 0:
        return f"*args{keystr(key_path[1:])}"
    else:
        kwarg_key = key_path[1]
        assert isinstance(kwarg_key, MappingKey)
        name = str(kwarg_key)[1:-1]  # get rid of the enclosed []
        return f"{name}{keystr(key_path[2:])}"
