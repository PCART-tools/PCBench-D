def full(g, sizes, value, dtype, layout, device, pin_memory=False):
    const_value = sym_help._maybe_get_const(value, "t")
    if sym_help._is_value(const_value):
        tmp = zeros(g, sizes, dtype, layout, device)
        return sym_opset9.add(g, tmp, value, g.op("Constant", value_t=torch.tensor(1)))
    else:
        dtype = sym_help._get_const(dtype, "i", "dtype")
        return _constant_fill(g, sizes, dtype, const_value)
