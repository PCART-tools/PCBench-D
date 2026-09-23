@onnx_impl(torch.sym_max, trace_only=True)
def sym_max(x: IntType, y: IntType) -> IntType:
    """sym_max(SymInt x, SymInt y) -> SymInt"""
    return op.Max(x, y)
