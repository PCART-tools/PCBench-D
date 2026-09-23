@torch.jit.script
def recurrent_scaleshift(x, scale, shift):
    y = x
    for i in range(64):
        y = scale * y + shift
    return y
