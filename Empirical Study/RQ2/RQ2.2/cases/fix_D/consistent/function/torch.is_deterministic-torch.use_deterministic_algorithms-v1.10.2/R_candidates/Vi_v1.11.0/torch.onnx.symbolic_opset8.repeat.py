def repeat(g, self, repeats):
    if not sym_help._is_value(repeats):
        repeats = g.op("Constant", value_t=torch.LongTensor(repeats))
    if sym_help._is_packed_list(repeats):
        repeat_size_len = len(sym_help._unpack_list(repeats))
    else:
        const_repeats = sym_help._maybe_get_const(repeats, "is")
        repeat_size_len = len(const_repeats)
    if self.isCompleteTensor():
        sizes = self.type().sizes()
        diff_dims = repeat_size_len - len(sizes)
        if diff_dims > 0:
            self = sym_opset9.view(g, self, g.op("Constant", value_t=torch.tensor([1] * diff_dims + sizes)))
    return g.op("Tile", self, repeats)
