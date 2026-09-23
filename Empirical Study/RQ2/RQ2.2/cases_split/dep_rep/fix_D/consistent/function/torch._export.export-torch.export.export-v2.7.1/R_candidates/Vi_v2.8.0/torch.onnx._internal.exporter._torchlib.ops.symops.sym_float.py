@onnx_impl(torch.sym_float, trace_only=True)
def sym_float(self: TensorType) -> FLOAT:
    """sym_float(SymInt self) -> SymFloat"""
    return op.Cast(self, to=FLOAT.dtype)
