def cat(g, tensor_list, dim):
    if sym_help._is_packed_list(tensor_list):
        from torch.onnx.symbolic_opset9 import cat as cat_opset9
        return cat_opset9(g, tensor_list, dim)
    else:
        dim = sym_help._get_const(dim, "i", "dim")
        return g.op("ConcatFromSequence", tensor_list, axis_i=dim)
