@onnx_impl(torch.sym_not, trace_only=True)
def sym_not(self: BOOL) -> BOOL:
    """sym_not(SymBool self) -> SymBool"""
    return op.Not(self)
