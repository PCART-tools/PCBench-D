@register_lowering(aten.sym_numel)
def sym_numel(a):
    return a.get_numel()
