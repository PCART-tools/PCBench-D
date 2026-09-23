@parse_args("v", "v", "v", "t", "t")
def addmm(g, self, mat1, mat2, beta, alpha):
    if _try_get_scalar_type(self):
        old_type, self, mat1, mat2 = _try_cast_integer_to_float(g, self, mat1, mat2)
        return _cast_to_type(
            g, g.op("Gemm", mat1, mat2, self,
                    beta_f=sym_help._scalar(beta), alpha_f=sym_help._scalar(alpha)), old_type)
    else:
        return g.op("Gemm", mat1, mat2, self, beta_f=sym_help._scalar(beta), alpha_f=sym_help._scalar(alpha))
