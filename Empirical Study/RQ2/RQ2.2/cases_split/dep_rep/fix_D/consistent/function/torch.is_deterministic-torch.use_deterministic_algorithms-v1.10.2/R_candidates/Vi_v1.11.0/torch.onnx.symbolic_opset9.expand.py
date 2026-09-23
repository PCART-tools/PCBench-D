def expand(g, self, size, implicit):
    size = sym_help._maybe_get_const(size, "is")
    if not sym_help._is_value(size):
        size = g.op("Constant", value_t=torch.LongTensor(size))
    elif sym_help._is_packed_list(size):
        # Expand with -1 dim value means dim is unchanged.
        # Since onnx::expand supports two-way broadcasting,
        # -1 dim value can be exported to onnx as 1
        size = sym_help._reshape_helper(g, stack(g, size, 0), g.op("Constant", value_t=torch.tensor([-1])))
    dtype = ScalarType.INT64
    ones = ones_like(g, size, dtype)
    neg_ones = mul(g, ones, g.op("Constant", value_t=torch.tensor(-1)))
    size = where(g, g.op("Equal", size, neg_ones), ones, size)
    return g.op("Expand", self, size)
