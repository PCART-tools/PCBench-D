@parse_args("v", "v", "v", "t", "t")
def addmm(g, self, mat1, mat2, beta, alpha):
    dtype = None
    self_dtype = sym_help._try_get_scalar_type(self)
    mat1_dtype = sym_help._try_get_scalar_type(mat1)
    mat2_dtype = sym_help._try_get_scalar_type(mat2)
    if self_dtype is not None:
        dtype = self_dtype
    elif mat1_dtype is not None:
        dtype = mat1_dtype
    elif mat2_dtype is not None:
        dtype = mat2_dtype

    mat1_rank = sym_help._get_tensor_rank(mat1)
    mat2_rank = sym_help._get_tensor_rank(mat2)

    def isNotNoneAnd(v, u):
        return v is not None and v != u

    if dtype is not None and (isNotNoneAnd(mat1_rank, 2) or isNotNoneAnd(mat2_rank, 2)):
        dtype = sym_help.scalar_type_to_onnx.index(sym_help.cast_pytorch_to_onnx[dtype])
        dtype = sym_help.scalar_type_to_pytorch_type[dtype]

        res1 = g.op("MatMul", mat1, mat2)
        res2 = self

        alpha = sym_help._scalar(alpha)
        beta = sym_help._scalar(beta)

        if alpha != 1:
            alpha = g.op("Constant",
                         value_t=torch.tensor(alpha, dtype=dtype))
            res1 = g.op("Mul", res1, alpha)
        if beta != 1:
            beta = g.op("Constant",
                        value_t=torch.tensor(sym_help._scalar(beta), dtype=dtype))
            res2 = g.op("Mul", res2, beta)

        return g.op("Add", res1, res2)

    return g.op("Gemm", mat1, mat2, self, beta_f=sym_help._scalar(beta), alpha_f=sym_help._scalar(alpha))
