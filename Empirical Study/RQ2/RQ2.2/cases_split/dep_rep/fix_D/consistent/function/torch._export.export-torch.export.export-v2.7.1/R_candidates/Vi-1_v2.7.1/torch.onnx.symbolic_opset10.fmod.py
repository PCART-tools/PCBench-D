@_onnx_symbolic("aten::fmod")
def fmod(g: jit_utils.GraphContext, input, other):
    return g.op("Mod", input, other, fmod_i=1)
