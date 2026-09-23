def baddbmm(g, self, batch1, batch2, beta, alpha):
    dtype = self.type().scalarType()
    batch_mul = matmul(g, batch1, batch2)
    mul_a = mul(g, batch_mul, g.op("Cast", alpha, to_i=sym_help.cast_pytorch_to_onnx[dtype]))
    mul_b = mul(g, self, g.op("Cast", beta, to_i=sym_help.cast_pytorch_to_onnx[dtype]))
    return add(g, mul_a, mul_b)
