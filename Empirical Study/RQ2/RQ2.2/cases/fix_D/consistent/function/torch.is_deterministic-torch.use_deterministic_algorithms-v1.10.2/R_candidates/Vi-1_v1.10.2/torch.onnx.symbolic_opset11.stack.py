def stack(g, tensor_list, dim):
    if sym_help._is_packed_list(tensor_list):
        from torch.onnx.symbolic_opset9 import stack as stack_opset9
        return stack_opset9(g, tensor_list, dim)
    else:
        dim = sym_help._get_const(dim, "i", "dim")
        return g.op("ConcatFromSequence", tensor_list, axis_i=dim, new_axis_i=1)
