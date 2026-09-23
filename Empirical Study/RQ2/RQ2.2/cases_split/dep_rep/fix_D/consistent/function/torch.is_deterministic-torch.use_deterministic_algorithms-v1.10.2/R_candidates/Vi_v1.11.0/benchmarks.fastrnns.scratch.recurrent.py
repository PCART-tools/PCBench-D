@torch.jit.script
def recurrent(x, scale, shift):
    y = x
    for i in range(100):
        y = fn(y, scale, shift)
    return y
