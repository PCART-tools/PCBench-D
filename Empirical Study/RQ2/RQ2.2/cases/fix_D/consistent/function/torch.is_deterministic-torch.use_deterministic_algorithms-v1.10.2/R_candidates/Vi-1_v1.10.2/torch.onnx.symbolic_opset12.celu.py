def celu(g, self, alpha):
    alpha = sym_help._maybe_get_const(alpha, "f")
    # if the input is of type double cast it to float
    if self.type().scalarType() == "Double":
        self = g.op("Cast", self, to_i=sym_help.cast_pytorch_to_onnx["Float"])
        out = g.op("Celu", self, alpha_f=alpha)
        return g.op("Cast", out, to_i=sym_help.cast_pytorch_to_onnx["Double"])

    return g.op("Celu", self, alpha_f=alpha)
