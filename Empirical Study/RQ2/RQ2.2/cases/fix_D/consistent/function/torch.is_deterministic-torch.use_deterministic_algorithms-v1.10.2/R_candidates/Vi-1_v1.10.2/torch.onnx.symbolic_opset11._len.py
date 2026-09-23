def _len(g, self):
    if _is_tensor_list(self) or self.node().kind() == "onnx::SplitToSequence":
        return g.op("SequenceLength", self)
    sz_0 = size(g, self, g.op("Constant", value_t=torch.LongTensor([0])))
    return sym_help._squeeze_helper(g, sz_0, [0])
