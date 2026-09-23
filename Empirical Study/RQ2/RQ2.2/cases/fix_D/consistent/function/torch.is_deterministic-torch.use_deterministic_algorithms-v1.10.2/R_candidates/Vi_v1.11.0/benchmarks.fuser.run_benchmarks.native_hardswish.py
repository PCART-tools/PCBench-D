def native_hardswish(a):
    return torch._C._nn.hardswish(a * 3)
