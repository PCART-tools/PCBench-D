@parse_args("v", "i", "none")
def cumsum(g, self, dim, dtype=None):
    dim_tensor = g.op("Constant", value_t=torch.tensor(dim, dtype=torch.int))
    if dtype and dtype.node().kind() != "prim::Constant":
        parsed_dtype = sym_help._get_const(dtype, "i", "dtype")
        cast = g.op("Cast", self, to_i=sym_help.scalar_type_to_onnx[parsed_dtype])
    else:
        cast = self
    csum = g.op("CumSum", cast, dim_tensor)
    return csum
