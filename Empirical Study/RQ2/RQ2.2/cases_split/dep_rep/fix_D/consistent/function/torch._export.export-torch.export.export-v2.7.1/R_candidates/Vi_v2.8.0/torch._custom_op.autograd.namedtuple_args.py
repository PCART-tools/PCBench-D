def namedtuple_args(schema, args):
    assert isinstance(args, tuple)
    tuple_cls = namedtuple_args_cls(schema)
    return tuple_cls(*args)
