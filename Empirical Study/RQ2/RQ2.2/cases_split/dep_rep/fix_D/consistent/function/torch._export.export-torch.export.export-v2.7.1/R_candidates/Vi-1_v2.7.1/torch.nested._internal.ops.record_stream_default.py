@register_jagged_func(torch.ops.aten.record_stream.default, "self: jt_all, s: any")
def record_stream_default(func, *args, **kwargs):
    inp = args[0]
    stream = args[1]
    # ensure all components live until stream computation completes
    func(inp._values, stream)
    func(inp._offsets, stream)
    if inp._lengths is not None:
        func(inp._lengths, stream)
