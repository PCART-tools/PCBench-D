@torch.fx.wrap
def _wrapped_linear(x, w, b):
    return F.linear(x, w, b)
