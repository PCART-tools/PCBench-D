def __getitem_(g, self, i):
    if sym_help._is_tensor_list(self):
        # SequenceAt requires that the input be a List of Tensors
        return g.op("SequenceAt", self, i)
    else:
        from torch.onnx.symbolic_opset9 import __getitem_ as getitem
        return getitem(g, self, i)
