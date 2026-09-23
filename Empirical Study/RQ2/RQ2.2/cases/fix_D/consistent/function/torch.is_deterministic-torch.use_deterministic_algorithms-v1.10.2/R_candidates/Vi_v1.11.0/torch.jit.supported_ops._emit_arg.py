def _emit_arg(indent, i, arg):
    v = "{} : {}".format(arg.name, _emit_type(arg.type))
    default = arg.default_value
    if default is not None:
        v = "{}={}".format(v, str(default))
    if i > 0:
        v = "\n{}{}".format(" " * indent, v)
    return v
