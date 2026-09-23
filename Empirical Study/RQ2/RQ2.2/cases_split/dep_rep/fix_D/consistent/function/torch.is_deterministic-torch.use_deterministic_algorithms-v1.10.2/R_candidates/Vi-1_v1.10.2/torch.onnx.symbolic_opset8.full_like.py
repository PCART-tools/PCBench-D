@parse_args("v", "f", "i", "v", "v", "v", "v")
def full_like(g, input, fill_value, dtype, layout, device, pin_memory=False, memory_format=None):
    shape = g.op("Shape", input)
    return _constant_fill(g, shape, dtype, fill_value)
