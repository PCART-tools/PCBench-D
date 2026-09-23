def reciprocal(g, self):
    # torch.reciprocal implicitly casts to float, so we do the same.
    if not sym_help._is_fp(self):
        self = g.op("Cast", self, to_i=sym_help.cast_pytorch_to_onnx["Float"])
    return g.op("Reciprocal", self)
