def call_op(op: Union[OpOverload, HopInstance], args, kwargs):
    if isinstance(op, OpOverload):
        return op(*args, **kwargs)

    assert isinstance(op, HopInstance), op
    schema = op._schema
    bound_args = list(args)
    bound_kwargs = {}
    for arg in schema.arguments[len(bound_args) :]:
        assert arg.name in kwargs, (arg.name, kwargs)
        val = kwargs[arg.name]
        if not arg.kwarg_only:
            bound_args.append(val)
        else:
            bound_kwargs[arg.name] = val

    if schema.tree_spec is not None:
        assert len(bound_args) == len(schema.arguments) and len(bound_kwargs) == 0
        args, kwargs = pytree.tree_unflatten(bound_args, schema.tree_spec)
        return op(*args, **kwargs)
    else:
        assert len(bound_args) + len(bound_kwargs) == len(schema.arguments)
        return op(*bound_args, **bound_kwargs)
