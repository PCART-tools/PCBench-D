@_onnx_symbolic("prim::convert_element_type")
def convert_element_type(g: jit_utils.GraphContext, self, *args):
    dtype = symbolic_helper._get_const(args[0], "i", "dtype")
    return g.op("Cast", self, to_i=_type_utils.JitScalarType(dtype).onnx_type())
