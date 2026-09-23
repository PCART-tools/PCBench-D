@_onnx_symbolic("aten::rand_like")
def rand_like(
    g: jit_utils.GraphContext,
    self,
    dtype,
    layout=None,
    device=None,
    pin_memory=False,
    memory_format=None,
):
    dtype = symbolic_helper._get_const(dtype, "i", "dtype")
    if dtype is None:
        dtype = _type_utils.JitScalarType.from_value(
            self, _type_utils.JitScalarType.FLOAT
        )
    return g.op(
        "RandomUniformLike", self, dtype_i=_type_utils.JitScalarType(dtype).onnx_type()
    )
