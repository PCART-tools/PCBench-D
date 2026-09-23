def full(g, sizes, value, dtype, layout, device, pin_memory=False):
    const_value = sym_help._maybe_get_const(value, "t")
    if sym_help._is_value(const_value):
        dtype = 6 if dtype is None else dtype
        tmp = zeros(g, sizes, dtype, layout, device)
        return add(g, tmp, value, g.op("Constant", value_t=torch.tensor(1)))
    else:
        dtype = sym_help._get_const(dtype, "i", "dtype")
        dtype = 6 if dtype is None else dtype
        return g.op("ConstantOfShape", sizes,
                    value_t=torch.tensor([const_value], dtype=sym_help.scalar_type_to_pytorch_type[dtype]))
