def add(g, self, other, alpha=None):
    if sym_help._is_value(self) and sym_help._is_tensor_list(self):
        tensor_list_node = other.node()
        if tensor_list_node.kind() != "prim::ListConstruct":
            return _unimplemented("add", "does not support adding dynamic tensor list to another")
        tensors = sym_help._unpack_list(other)
        l = self
        for t in tensors:
            l = g.op("SequenceInsert", l, t)
        return l

    return torch.onnx.symbolic_opset9.add(g, self, other, alpha)
