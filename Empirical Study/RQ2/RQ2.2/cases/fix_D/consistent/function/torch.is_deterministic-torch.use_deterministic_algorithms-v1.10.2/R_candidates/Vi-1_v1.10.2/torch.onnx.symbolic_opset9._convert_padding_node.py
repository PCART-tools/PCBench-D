def _convert_padding_node(padding):
    padding = sym_help._maybe_get_const(padding, "is")
    if sym_help._is_value(padding) and sym_help._is_packed_list(padding):
        input_list = sym_help._unpack_list(padding)
        try:
            padding = [sym_help._get_const(v, "i", "padding") for v in input_list]
        except Exception:
            return sym_help._onnx_opset_unsupported_detailed("Pad", 9, 11, "The sizes of the padding must be constant")
    return padding
