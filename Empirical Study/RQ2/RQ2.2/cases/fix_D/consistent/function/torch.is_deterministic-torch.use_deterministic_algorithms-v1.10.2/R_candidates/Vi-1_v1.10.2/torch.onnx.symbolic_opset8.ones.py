@parse_args("v", "i", "v", "v", "v")
def ones(g, sizes, dtype, layout, device, pin_memory=False):
    return _constant_fill(g, sizes, dtype, 1)
