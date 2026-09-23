@torch.jit.script
def torch_sumall(a, iterations):
    # type: (Tensor, int)
    result = 0.0
    for _ in range(iterations):
        result += float(torch.sum(a))
        a[0][0] += 0.01
    return result
