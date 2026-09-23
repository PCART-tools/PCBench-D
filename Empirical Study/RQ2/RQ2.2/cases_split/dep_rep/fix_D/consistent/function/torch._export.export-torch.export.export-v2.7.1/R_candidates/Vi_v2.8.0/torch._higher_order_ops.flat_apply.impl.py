def impl(func, in_spec, *flat_args):
    if not isinstance(func, _op_types):
        # assume _ConstantFunction
        func = pytree._retrieve_constant(func)
        assert isinstance(func, _ConstantFunction)

    args, kwargs = from_graphable(flat_args, in_spec)
    out = func(*args, **kwargs)

    # Right now, all outputs must either be graphable or lists/tuples of graphables.
    #
    # TODO: The following can be updated to support non-graphable outputs and pytrees.
    # For non-graphable constant outputs: the assumption would be that they are constant
    # (everytime the function runs those MUST be the same)
    # For pytree outputs:
    # I'm not sure if we need to return (flat_output, spec) or just (flat_output,):
    # in the latter case the tracers need to carry out the output specs
    # (they need to know how to reconstruct the object from just the flat_output).
    def is_valid_output(x):
        if isinstance(x, (tuple, list)):
            return all(map(is_valid_output, x))
        return is_graphable(x)

    assert is_valid_output(out)
    return out
