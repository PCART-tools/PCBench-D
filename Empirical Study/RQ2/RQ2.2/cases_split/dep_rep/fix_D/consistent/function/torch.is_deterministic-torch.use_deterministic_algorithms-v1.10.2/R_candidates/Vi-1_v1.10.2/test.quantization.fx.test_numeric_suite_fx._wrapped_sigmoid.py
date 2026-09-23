@torch.fx.wrap
def _wrapped_sigmoid(x):
    return F.sigmoid(x)
