@_onnx_symbolic("aten::baddbmm")
def baddbmm(g: jit_utils.GraphContext, self, batch1, batch2, beta, alpha):
    scalar_type = _type_utils.JitScalarType.from_value(self)
    batch_mul = matmul(g, batch1, batch2)
    mul_a = mul(
        g,
        batch_mul,
        g.op("Cast", alpha, to_i=scalar_type.onnx_type()),
    )
    mul_b = mul(
        g,
        self,
        g.op("Cast", beta, to_i=scalar_type.onnx_type()),
    )
    return add(g, mul_a, mul_b)
