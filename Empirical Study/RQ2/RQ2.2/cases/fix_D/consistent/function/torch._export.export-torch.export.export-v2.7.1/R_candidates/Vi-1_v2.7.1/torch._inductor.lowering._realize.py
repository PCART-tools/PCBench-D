@register_lowering(torch.ops._inductor_test.realize)
def _realize(x):
    x.realize()
    return clone(x)
