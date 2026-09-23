def full(g, sizes, value, dtype, layout, device, pin_memory=False):
    const_value = sym_help._maybe_get_const(value, "t")
    if sym_help._is_value(const_value):
        dtype = ScalarType.FLOAT if dtype is None else dtype
        tmp = zeros(g, sizes, dtype, layout, device)
        return add(g, tmp, value, g.op("Constant", value_t=torch.tensor(1)))
    else:
        dtype = sym_help._get_const(dtype, "i", "dtype")
        dtype = ScalarType.FLOAT if dtype is None else dtype
        sizes_ = sym_help._maybe_get_const(sizes, "is")
        if isinstance(sizes_, list) and len(sizes_) == 0:
            sizes = g.op("Constant", value_t=torch.tensor([]).to(torch.int64))
        return g.op("ConstantOfShape", sizes,
                    value_t=const_value.view(1).to(sym_help.scalar_type_to_pytorch_type[dtype]))
