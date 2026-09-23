@parse_args("v", "i", "v", "v", "v", "v")
def empty_like(g, input, dtype, layout, device, pin_memory=False, memory_format=None):
    return zeros_like(g, input, dtype, layout, device, pin_memory)
