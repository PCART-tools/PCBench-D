@torch.fx.wrap
def _wrapped_hardswish(x):
    return F.hardswish(x)
