def narrow(g, input, dim, start, length):
    from torch.onnx.symbolic_helper import _slice_helper
    end = g.op("Add", start, length)
    return _slice_helper(g, input, axes=dim, starts=start, ends=end, dynamic_slice=True)
