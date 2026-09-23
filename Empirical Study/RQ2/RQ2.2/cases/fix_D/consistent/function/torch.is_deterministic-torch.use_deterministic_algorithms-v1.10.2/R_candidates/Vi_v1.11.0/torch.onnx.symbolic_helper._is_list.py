def _is_list(x):
    return isinstance(x.type(), torch._C.ListType)
