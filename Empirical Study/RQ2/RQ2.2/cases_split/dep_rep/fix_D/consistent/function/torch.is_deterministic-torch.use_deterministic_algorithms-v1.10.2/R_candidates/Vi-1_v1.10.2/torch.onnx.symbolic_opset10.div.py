def div(g, self, other, *args):
    if len(args) == 0:
        return torch.onnx.symbolic_opset9.true_divide(g, self, other)
    else:
        return _div_rounding_mode(g, self, other, *args)
