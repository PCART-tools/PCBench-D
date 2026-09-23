def _is_constant(value):
    return not _is_value(value) or value.node().kind() in ('onnx::Constant', 'prim::Constant')
