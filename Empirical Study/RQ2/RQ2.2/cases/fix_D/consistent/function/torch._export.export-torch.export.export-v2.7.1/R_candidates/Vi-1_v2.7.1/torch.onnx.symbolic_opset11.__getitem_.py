@_onnx_symbolic("aten::__getitem_")
def __getitem_(g: jit_utils.GraphContext, self, i):
    if symbolic_helper._is_tensor_list(self):
        # SequenceAt requires that the input be a List of Tensors
        return g.op("SequenceAt", self, i)
    else:
        from torch.onnx.symbolic_opset9 import __getitem_ as getitem

        return getitem(g, self, i)
