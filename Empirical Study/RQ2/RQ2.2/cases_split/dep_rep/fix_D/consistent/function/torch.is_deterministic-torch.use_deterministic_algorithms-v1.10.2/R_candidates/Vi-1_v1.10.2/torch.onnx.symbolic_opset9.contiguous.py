@parse_args("v", "i")
def contiguous(g, input, memory_format):
    if memory_format > 2:  # allower values are any, preserve and contiguous_format
        raise RuntimeError("onnx memory_format support is not implemented")
    return input
