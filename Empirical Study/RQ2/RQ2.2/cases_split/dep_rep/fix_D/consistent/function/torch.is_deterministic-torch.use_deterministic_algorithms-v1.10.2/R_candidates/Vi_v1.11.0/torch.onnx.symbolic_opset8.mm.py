def mm(g, self, other):
    # Create a dummy C tensor. Only needed for API purposes, the value is
    # since beta = 0
    ty = sym_help._try_get_scalar_type(self, other).lower()
    C = g.constant(0, [1], ty)
    if _try_get_scalar_type(self):
        old_type, self, other, C = _try_cast_integer_to_float(g, self, other, C)
        return _cast_to_type(g, g.op("Gemm", self, other, C, beta_f=0.0, alpha_f=1.0), old_type)
    else:
        return g.op("Gemm", self, other, C, beta_f=0.0, alpha_f=1.0)
