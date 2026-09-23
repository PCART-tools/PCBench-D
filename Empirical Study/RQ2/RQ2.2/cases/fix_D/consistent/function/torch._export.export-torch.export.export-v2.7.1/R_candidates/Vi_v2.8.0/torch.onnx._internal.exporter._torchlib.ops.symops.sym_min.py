@onnx_impl(torch.sym_min, trace_only=True)
def sym_min(x: IntType, y: IntType) -> IntType:
    """sym_min(SymInt x, SymInt y) -> SymInt"""
    return op.Min(x, y)
