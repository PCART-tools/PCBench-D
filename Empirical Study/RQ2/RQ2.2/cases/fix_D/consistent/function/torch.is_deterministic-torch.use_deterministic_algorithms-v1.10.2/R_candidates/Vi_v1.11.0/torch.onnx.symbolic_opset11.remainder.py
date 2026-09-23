def remainder(g, input, other):
    if sym_help._is_fp(input) or sym_help._is_fp(other):
        from torch.onnx.symbolic_opset9 import remainder as _remainder_9
        return _remainder_9(g, input, other)
    return g.op("Mod", input, other, fmod_i=0)
