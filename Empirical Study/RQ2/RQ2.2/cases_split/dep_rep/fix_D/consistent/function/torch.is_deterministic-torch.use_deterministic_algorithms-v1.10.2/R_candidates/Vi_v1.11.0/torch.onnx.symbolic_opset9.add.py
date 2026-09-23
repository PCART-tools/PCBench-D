def add(g, self, other, alpha=None):
    if sym_help._is_value(self) and sym_help._is_tensor_list(self):
        return sym_help._onnx_opset_unsupported_detailed("Add", 9, 11, "Add between list of tensors not supported")

    # default alpha arg is to allow no-alpha add (aten add st overload no alpha)
    if alpha and sym_help._scalar(sym_help._maybe_get_scalar(alpha)) != 1:
        return _unimplemented("add", "alpha != 1")
    return g.op("Add", self, other)
