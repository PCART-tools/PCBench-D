def _set_tf_attr(attr_dict, arg):
    '''
    Add attributes to a node. Key is the arg.name, and values can be shape,
        floats, strings, ints or an empty list.

    Args:
        attr_dict: Dictionary to update (usually attributes of a Node)
        arg: Object with name and data fields.

    Returns:
        None. Modifies attr_dict in-place.
    '''
    k = arg.name
    if k == 'shape' and arg.ints:
        _add_tf_shape(attr_dict, arg.ints)
        return
    # Float
    if arg.HasField("f"):
        attr_dict[k].f = arg.f
        return
    # Integer
    if arg.HasField("i"):
        attr_dict[k].i = arg.i
        return
    # String
    if arg.HasField("s"):
        attr_dict[k].s = (
            arg.s if isinstance(arg.s, bytes) else str(arg.s).encode('utf-8')
        )
        return
    if arg.floats:
        attr_dict[k].list.f.extend(arg.floats)
        return
    if arg.ints:
        attr_dict[k].list.i.extend(arg.ints)
        return
    if arg.strings:
        attr_dict[k].list.s.extend(
            s if isinstance(s, bytes) else str(s).encode('utf-8')
            for s in arg.strings
        )
        return
    # The value is an empty list.
    attr_dict[k].list.s.extend([])
