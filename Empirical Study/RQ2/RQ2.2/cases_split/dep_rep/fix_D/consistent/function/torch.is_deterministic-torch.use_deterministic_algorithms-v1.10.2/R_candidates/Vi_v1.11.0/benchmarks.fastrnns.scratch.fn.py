@torch.jit.script
def fn(x, scale, shift):
    return scale * x / shift
