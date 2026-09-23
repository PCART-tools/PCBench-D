@parse_args("v", "i", "v", "v")
def scatter_add(g, self, dim, index, src):
    dtype = sym_help._try_get_scalar_type(self)
    if dtype is None:
        return _unimplemented("scatter_add", "input dtype not accessible")
    dtype = sym_help.scalar_type_to_onnx.index(sym_help.cast_pytorch_to_onnx[dtype])
    dtype = sym_help.scalar_type_to_pytorch_type[dtype]
    sizes = sym_help._get_tensor_sizes(self, allow_nonstatic=False)
    if sizes:
        to_add = g.op("Constant", value_t=torch.zeros(sizes, dtype=dtype))
    else:
        dtype = sym_help.scalar_type_to_pytorch_type.index(dtype)
        to_add = zeros_like(g, self, dtype)
    to_add = sym_help._scatter_helper(g, to_add, dim, index, src)
    return add(g, self, to_add)
