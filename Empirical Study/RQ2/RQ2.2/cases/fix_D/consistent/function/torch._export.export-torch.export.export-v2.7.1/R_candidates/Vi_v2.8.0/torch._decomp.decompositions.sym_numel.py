@register_decomposition(aten.sym_numel)
def sym_numel(t):
    return functools.reduce(operator.mul, t.shape, 1)
