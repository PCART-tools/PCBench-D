@parse_args("v", "i", "v", "v", "v")
def ones(g, sizes, dtype, layout, device, pin_memory=False):
    if dtype is None:
        dtype = ScalarType.FLOAT
    sizes_ = sym_help._maybe_get_const(sizes, "is")
    if isinstance(sizes_, list) and len(sizes_) == 0:
        sizes = g.op("Constant", value_t=torch.tensor([]).to(torch.int64))
    return g.op("ConstantOfShape", sizes,
                value_t=torch.tensor([1], dtype=sym_help.scalar_type_to_pytorch_type[dtype]))
