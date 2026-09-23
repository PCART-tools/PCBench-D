def true_divide(g, self, other):
    # Case 1: both values are floating
    # Performs div as usual
    if sym_help._is_fp(self) and sym_help._is_fp(other):
        return g.op("Div", self, other)

    # Case 2: self is floating, other is not
    # Casts other to self's dtype
    if sym_help._is_fp(self):
        other = g.op("Cast", other, to_i=sym_help.cast_pytorch_to_onnx[self.type().scalarType()])
        return g.op("Div", self, other)

    # Case 3: other is floating, self is not
    # Casts self to other's dtype
    if sym_help._is_fp(other):
        self = g.op("Cast", self, to_i=sym_help.cast_pytorch_to_onnx[other.type().scalarType()])
        return g.op("Div", self, other)

    # Case 4: neither is floating
    # Casts both inputs to the default scalar type
    scalar_type = torch.get_default_dtype()
    onnx_scalar_type = sym_help.cast_pytorch_to_onnx["Float"]
    assert scalar_type is torch.float or scalar_type is torch.double
    if torch.get_default_dtype() is torch.double:
        onnx_scalar_type = sym_help.cast_pytorch_to_onnx["Double"]

    self = g.op("Cast", self, to_i=onnx_scalar_type)
    other = g.op("Cast", other, to_i=onnx_scalar_type)
    return g.op("Div", self, other)
