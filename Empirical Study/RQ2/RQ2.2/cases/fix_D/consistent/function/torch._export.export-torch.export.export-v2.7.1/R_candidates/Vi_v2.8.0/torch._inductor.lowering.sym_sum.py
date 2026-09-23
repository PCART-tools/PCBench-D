@register_lowering(torch.sym_sum)
def sym_sum(args):
    return sympy.Add(*args)
