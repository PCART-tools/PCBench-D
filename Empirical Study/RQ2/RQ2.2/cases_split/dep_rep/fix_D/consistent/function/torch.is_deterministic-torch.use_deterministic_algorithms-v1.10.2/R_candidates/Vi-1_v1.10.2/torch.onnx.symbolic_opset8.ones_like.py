@parse_args("v", "i", "v", "v", "v", "v")
def ones_like(g, input, dtype, layout, device, pin_memory=False, memory_format=None):
    shape = g.op("Shape", input)
    return _constant_fill(g, shape, dtype, 1)
