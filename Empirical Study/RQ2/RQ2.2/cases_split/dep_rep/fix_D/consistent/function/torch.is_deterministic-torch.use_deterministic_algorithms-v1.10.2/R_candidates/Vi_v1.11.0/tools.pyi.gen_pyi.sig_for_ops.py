def sig_for_ops(opname: str) -> List[str]:
    """sig_for_ops(opname : str) -> List[str]

    Returns signatures for operator special functions (__add__ etc.)"""

    # we have to do this by hand, because they are hand-bound in Python

    assert opname.endswith('__') and opname.startswith('__'), "Unexpected op {}".format(opname)

    name = opname[2:-2]
    if name in binary_ops:
        return ['def {}(self, other: Any) -> Tensor: ...'.format(opname)]
    elif name in comparison_ops:
        sig = 'def {}(self, other: Any) -> Tensor: ...'.format(opname)
        if name in symmetric_comparison_ops:
            # unsafe override https://github.com/python/mypy/issues/5704
            sig += '  # type: ignore[override]'
        return [sig]
    elif name in unary_ops:
        return ['def {}(self) -> Tensor: ...'.format(opname)]
    elif name in to_py_type_ops:
        if name in {'bool', 'float', 'complex'}:
            tname = name
        elif name == 'nonzero':
            tname = 'bool'
        else:
            tname = 'int'
        if tname in {'float', 'int', 'bool', 'complex'}:
            tname = 'builtins.' + tname
        return ['def {}(self) -> {}: ...'.format(opname, tname)]
    else:
        raise Exception("unknown op", opname)
