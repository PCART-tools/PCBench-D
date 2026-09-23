def _set_tf_attr(m, arg):
    k = arg.name
    if k == 'shape' and arg.ints:
        _add_tf_shape(m, arg.ints)
        return
    if arg.HasField("f"):
        m[k].f = arg.f
        return
    if arg.HasField("i"):
        m[k].i = arg.i
        return
    if arg.HasField("s"):
        m[k].s = (
            arg.s if isinstance(arg.s, bytes) else str(arg.s).encode('utf-8')
        )
        return
    if arg.floats:
        m[k].list.f.extend(arg.floats)
        return
    if arg.ints:
        m[k].list.i.extend(arg.ints)
        return
    if arg.strings:
        m[k].list.s.extend(
            s if isinstance(s, bytes) else str(s).encode('utf-8')
            for s in arg.strings
        )
        return
    # The value is an empty list.
    m[k].list.s.extend([])
