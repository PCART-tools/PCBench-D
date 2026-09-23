def _arg_val(arg):
    if arg.HasField('f'):
        return str(arg.f)
    if arg.HasField('i'):
        return str(arg.i)
    if arg.HasField('s'):
        return _sanitize_str(arg.s)
    if arg.floats:
        return str(list(arg.floats))
    if arg.ints:
        return str(list(arg.ints))
    if arg.strings:
        return str([_sanitize_str(s) for s in arg.strings])
    return '[]'
